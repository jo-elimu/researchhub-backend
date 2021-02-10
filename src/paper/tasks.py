from psycopg2.errors import UniqueViolation

import fitz
import logging
import os
import re
import requests
import shutil
import twitter
import urllib.request
import feedparser
import time

from io import BytesIO
from slugify import slugify
from datetime import datetime, timedelta, timezone
from subprocess import call
from PIL import Image
from habanero import Crossref
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger

from django.apps import apps
from django.core.cache import cache
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import IntegrityError
from django.http.request import HttpRequest
from rest_framework.request import Request
from discussion.models import Thread, Comment
from purchase.models import Wallet
from researchhub.celery import app
from researchhub.settings import APP_ENV


from paper.utils import (
    check_crossref_title,
    check_pdf_title,
    get_pdf_from_url,
    get_crossref_results,
    fitz_extract_figures,
    merge_paper_bulletpoints,
    merge_paper_threads,
    merge_paper_votes,
    get_cache_key,
    clean_abstract,
    get_csl_item,
    get_redirect_url
)
from utils import sentry
from utils.arxiv.categories import get_category_name, ARXIV_CATEGORIES, get_general_hub_name
from utils.crossref import get_crossref_issued_date
from utils.twitter import (
    get_twitter_url_results,
    get_twitter_results,
    get_twitter_search_rate_limit
)
from utils.http import check_url_contains_pdf

logger = get_task_logger(__name__)


@app.task
def censored_paper_cleanup(paper_id):
    Paper = apps.get_model('paper.Paper')
    paper = Paper.objects.filter(id=paper_id).first()

    if not paper.is_removed:
        paper.is_removed = True
        paper.save()

    if paper:
        paper.votes.update(is_removed=True)
        for vote in paper.votes.all():
            if vote.vote_type == 1:
                user = vote.created_by
                user.set_probable_spammer()

        uploaded_by = paper.uploaded_by
        uploaded_by.set_probable_spammer()


@app.task
def download_pdf(paper_id, retry=0):
    if retry > 3:
        return

    Paper = apps.get_model('paper.Paper')
    paper = Paper.objects.get(id=paper_id)
    paper_url = paper.url
    pdf_url = paper.pdf_url
    url = pdf_url or paper_url
    url_has_pdf = (check_url_contains_pdf(paper_url) or pdf_url)

    if paper_url and url_has_pdf:
        try:
            pdf = get_pdf_from_url(url)
            filename = paper.url.split('/').pop()
            if not filename.endswith('.pdf'):
                filename += '.pdf'
            paper.file.save(filename, pdf)
            paper.save(update_fields=['file'])
            paper.extract_pdf_preview(use_celery=True)
        except Exception as e:
            sentry.log_info(e)
            download_pdf.apply_async(
                (paper.id, retry + 1),
                priority=3,
                countdown=15 * (retry + 1)
            )


@app.task
def add_references(paper_id):
    if paper_id is None:
        return

    Paper = apps.get_model('paper.Paper')
    paper = Paper.objects.get(id=paper_id)
    paper.add_references()


@app.task
def add_orcid_authors(paper_id):
    if paper_id is None:
        return

    from utils.orcid import orcid_api

    Paper = apps.get_model('paper.Paper')
    paper = Paper.objects.get(id=paper_id)
    orcid_authors = []
    while True:
        doi = paper.doi
        if doi is not None:
            orcid_authors = orcid_api.get_authors(doi=doi)
            if orcid_authors:
                break

        arxiv_id = paper.alternate_ids.get('arxiv', None)
        if arxiv_id is not None and doi:
            orcid_authors = orcid_api.get_authors(arxiv=doi)
            if orcid_authors:
                break

        if arxiv_id is not None:
            orcid_authors = orcid_api.get_authors(arxiv=arxiv_id)
            if orcid_authors:
                break

        break

        if len(orcid_authors) < 1:
            print('No authors to add')
            logging.info('Did not find paper identifier to give to ORCID API')

    paper.authors.add(*orcid_authors)
    for author in paper.authors.iterator():
        Wallet.objects.get_or_create(author=author)
    logging.info(f'Finished adding orcid authors to paper {paper.id}')


@app.task
def celery_extract_figures(paper_id):
    if paper_id is None:
        return

    Paper = apps.get_model('paper.Paper')
    Figure = apps.get_model('paper.Figure')
    paper = Paper.objects.get(id=paper_id)

    file = paper.file
    if not file:
        return

    path = f'/tmp/figures/{paper_id}/'
    filename = f'{paper.id}.pdf'
    file_path = f'{path}{filename}'
    file_url = file.url

    if not os.path.isdir(path):
        os.mkdir(path)

    try:
        res = requests.get(file_url)
        with open(file_path, 'wb+') as f:
            f.write(res.content)

        fitz_extract_figures(file_path)

        figures = os.listdir(path)
        if len(figures) == 1:  # Only the pdf exists
            args = [
                'java',
                '-jar',
                'pdffigures2-assembly-0.1.0.jar',
                file_path,
                '-m',
                path,
                '-d',
                path,
                '-e'
            ]
            call(args)
            figures = os.listdir(path)

        for extracted_figure in figures:
            extracted_figure_path = f'{path}{extracted_figure}'
            if '.png' in extracted_figure:
                with open(extracted_figure_path, 'rb') as f:
                    extracted_figures = Figure.objects.filter(paper=paper)
                    if not extracted_figures.filter(
                        file__contains=f.name,
                        figure_type=Figure.FIGURE
                    ):
                        Figure.objects.create(
                            file=File(f),
                            paper=paper,
                            figure_type=Figure.FIGURE
                        )
    except Exception as e:
        sentry.log_error(e)
    finally:
        shutil.rmtree(path)
        cache_key = get_cache_key(None, 'figure', pk=paper_id)
        cache.delete(cache_key)


@app.task
def celery_extract_pdf_preview(paper_id, retry=0):
    if paper_id is None or retry > 2:
        print('No paper id for pdf preview')
        return False

    print(f'Extracting pdf figures for paper: {paper_id}')

    Paper = apps.get_model('paper.Paper')
    Figure = apps.get_model('paper.Figure')
    paper = Paper.objects.get(id=paper_id)

    file = paper.file
    if not file:
        print(f'No file exists for paper: {paper_id}')
        celery_extract_pdf_preview.apply_async(
            (paper.id, retry + 1),
            priority=3,
            countdown=10,
        )
        return False

    file_url = file.url

    try:
        res = requests.get(file_url)
        doc = fitz.open(stream=res.content, filetype='pdf')
        extracted_figures = Figure.objects.filter(paper=paper)
        for page in doc:
            pix = page.getPixmap(alpha=False)
            output_filename = f'{paper_id}-{page.number}.jpg'

            if not extracted_figures.filter(
                file__contains=output_filename,
                figure_type=Figure.PREVIEW
            ):
                img_buffer = BytesIO()
                img_buffer.write(pix.getImageData(output='jpg'))
                image = Image.open(img_buffer)
                image.save(img_buffer, 'jpeg', quality=0)
                file = ContentFile(
                    img_buffer.getvalue(),
                    name=output_filename
                )
                Figure.objects.create(
                    file=file,
                    paper=paper,
                    figure_type=Figure.PREVIEW
                )
    except Exception as e:
        sentry.log_error(e)
    finally:
        cache_key = get_cache_key(None, 'figure', pk=paper_id)
        cache.delete(cache_key)
    return True


@app.task
def celery_extract_meta_data(paper_id, title, check_title):
    if paper_id is None:
        return

    Paper = apps.get_model('paper.Paper')
    date_format = '%Y-%m-%dT%H:%M:%SZ'
    paper = Paper.objects.get(id=paper_id)

    if check_title:
        has_title = check_pdf_title(title, paper.file)
        if not has_title:
            return

    best_matching_result = get_crossref_results(title, index=1)[0]

    try:
        if 'title' in best_matching_result:
            crossref_title = best_matching_result.get('title', [''])[0]
        else:
            crossref_title = best_matching_result.get('container-title', [''])
            crossref_title = crossref_title[0]

        similar_title = check_crossref_title(title, crossref_title)

        if not similar_title:
            return

        if not paper.doi:
            doi = best_matching_result.get('DOI', paper.doi)
            paper.doi = doi

        url = best_matching_result.get('URL', None)
        publish_date = best_matching_result['created']['date-time']
        publish_date = datetime.strptime(publish_date, date_format).date()
        tagline = best_matching_result.get('abstract', '')
        tagline = re.sub(r'<[^<]+>', '', tagline)  # Removing any jat xml tags

        paper.url = url
        paper.paper_publish_date = publish_date

        if not paper.tagline:
            paper.tagline = tagline

        paper_cache_key = get_cache_key(None, 'paper', pk=paper_id)
        cache.delete(paper_cache_key)

        paper.check_doi()
        paper.save()
    except (UniqueViolation, IntegrityError) as e:
        sentry.log_info(e)
    except Exception as e:
        sentry.log_info(e)


@app.task
def celery_extract_twitter_comments(paper_id):
    # TODO: Optimize this
    return

    if paper_id is None:
        return

    Paper = apps.get_model('paper.Paper')
    paper = Paper.objects.get(id=paper_id)
    url = paper.url
    if not url:
        return

    source = 'twitter'
    try:

        results = get_twitter_url_results(url)
        for res in results:
            source_id = res.id_str
            username = res.user.screen_name
            text = res.full_text
            thread_user_profile_img = res.user.profile_image_url_https
            thread_created_date = res.created_at_in_seconds
            thread_created_date = datetime.fromtimestamp(
                thread_created_date,
                timezone.utc
            )

            thread_exists = Thread.objects.filter(
                external_metadata__source_id=source_id
            ).exists()

            if not thread_exists:
                external_thread_metadata = {
                    'source_id': source_id,
                    'username': username,
                    'picture': thread_user_profile_img,
                    'url': f'https://twitter.com/{username}/status/{source_id}'
                }
                thread = Thread.objects.create(
                    paper=paper,
                    source=source,
                    external_metadata=external_thread_metadata,
                    plain_text=text,
                )
                thread.created_date = thread_created_date
                thread.save()

                query = f'to:{username}'
                replies = get_twitter_results(query)
                for reply in replies:
                    reply_username = reply.user.screen_name
                    reply_id = reply.id_str
                    reply_text = reply.full_text
                    comment_user_img = reply.user.profile_image_url_https
                    comment_created_date = reply.created_at_in_seconds
                    comment_created_date = datetime.fromtimestamp(
                        comment_created_date,
                        timezone.utc
                    )

                    reply_exists = Comment.objects.filter(
                        external_metadata__source_id=reply_id
                    ).exists()

                    if not reply_exists:
                        external_comment_metadata = {
                            'source_id': reply_id,
                            'username': reply_username,
                            'picture': comment_user_img,
                            'url': f'https://twitter.com/{reply_username}/status/{reply_id}'
                        }
                        comment = Comment.objects.create(
                            parent=thread,
                            source=source,
                            external_metadata=external_comment_metadata,
                            plain_text=reply_text,
                        )
                        comment.created_date = comment_created_date
                        comment.save()
    except twitter.TwitterError:
        # TODO: Do we want to push the call back to celery if it exceeds the
        # rate limit?
        return


@app.task(queue=f'{APP_ENV}_autopull_queue')
def celery_calculate_paper_twitter_score(paper_id, iteration=0):
    if paper_id is None or iteration > 2:
        return

    remaining, seconds = get_twitter_search_rate_limit()
    if remaining < 1:
        celery_calculate_paper_twitter_score.apply_async(
            (paper_id, iteration),
            priority=5,
            countdown=seconds + 5
        )
        return False

    Paper = apps.get_model('paper.Paper')
    paper = Paper.objects.get(id=paper_id)

    try:
        twitter_score = paper.calculate_twitter_score()
    except Exception as e:
        remaining, seconds = get_twitter_search_rate_limit()
        celery_calculate_paper_twitter_score.apply_async(
            (paper_id, iteration),
            priority=5,
            countdown=seconds + 5
        )
        return False

    celery_calculate_paper_twitter_score.apply_async(
        (paper_id, iteration + 1),
        priority=5,
        countdown=86400 * (iteration + 1)
    )
    score = paper.calculate_score()
    paper.score = score
    paper.save()

    if score > 0:
        paper.calculate_hot_score()
    paper_cache_key = get_cache_key(None, 'paper', pk=paper.id)
    cache.delete(paper_cache_key)


@app.task
def handle_duplicate_doi(new_paper, doi):
    Paper = apps.get_model('paper.Paper')
    original_paper = Paper.objects.filter(doi=doi).order_by('uploaded_date')[0]
    merge_paper_votes(original_paper, new_paper)
    merge_paper_threads(original_paper, new_paper)
    merge_paper_bulletpoints(original_paper, new_paper)
    new_paper.delete()


# @periodic_task(
#     run_every=crontab(minute='*/30'),
#     priority=2,
#     options={'queue': APP_ENV}
# )
# TODO: Remove this completely?
def celery_preload_hub_papers():
    # hub_ids = Hub.objects.values_list('id', flat=True)
    hub_ids = [0]
    orderings = (
        '-hot_score',
        '-score',
        '-discussed',
        '-uploaded_date',
    )
    filter_types = (
        'year',
        'month',
        'week',
        'today',
    )

    start_date_hour = 7
    end_date = today = datetime.now()
    for hub_id in hub_ids:
        for ordering in orderings:
            for filter_type in filter_types:
                cache_pk = f'{hub_id}_{ordering}_{filter_type}'
                if filter_type == 'year':
                    td = timedelta(days=365)
                elif filter_type == 'month':
                    td = timedelta(days=30)
                elif filter_type == 'week':
                    td = timedelta(days=7)
                else:
                    td = timedelta(days=0)

                cache_key = get_cache_key(None, 'hub', pk=cache_pk)
                datetime_diff = today - td
                year = datetime_diff.year
                month = datetime_diff.month
                day = datetime_diff.day
                start_date = datetime(
                    year,
                    month,
                    day,
                    hour=start_date_hour
                )

                args = (
                    1,
                    start_date,
                    end_date,
                    ordering,
                    hub_id,
                    {},
                    {},
                    cache_key
                )
                preload_hub_papers(*args)
                break
            break
        break


@app.task
def preload_hub_papers(
    page_number,
    start_date,
    end_date,
    ordering,
    hub_id,
    meta=None,
    synchronous=False,
):
    from paper.serializers import HubPaperSerializer
    from paper.views import PaperViewSet
    paper_view = PaperViewSet()
    http_req = HttpRequest()
    if meta:
        http_req.META = meta
    else:
        http_req.META = {'SERVER_NAME': 'localhost', 'SERVER_PORT': 80}
    paper_view.request = Request(http_req)
    papers = paper_view._get_filtered_papers(hub_id, ordering)
    order_papers = paper_view.calculate_paper_ordering(
        papers,
        ordering,
        start_date,
        end_date
    )

    context = {}
    context['user_no_balance'] = True

    page = paper_view.paginate_queryset(order_papers)
    serializer = HubPaperSerializer(page, many=True, context=context)
    serializer_data = serializer.data
    paginated_response = paper_view.get_paginated_response(
        {'data': serializer_data, 'no_results': False, 'feed_type': 'all'}
    )

    if synchronous:
        time_difference = end_date - start_date
    else:
        now = datetime.now()
        time_difference = now - now
    cache_pk = ''
    if time_difference.days > 365:
        cache_pk = f'{hub_id}_{ordering}_all_time'
    elif time_difference.days == 365:
        cache_pk = f'{hub_id}_{ordering}_year'
    elif time_difference.days == 30 or time_difference.days == 31:
        cache_pk = f'{hub_id}_{ordering}_month'
    elif time_difference.days == 7:
        cache_pk = f'{hub_id}_{ordering}_week'
    else:
        cache_pk = f'{hub_id}_{ordering}_today'

    cache_key_hub = get_cache_key(None, 'hub', pk=cache_pk)
    if cache_key_hub:
        cache.set(
            cache_key_hub,
            paginated_response.data,
            timeout=60*40
        )

    return paginated_response.data


# ARXIV Download Constants
RESULTS_PER_ITERATION = 50 # default is 10, if this goes too high like >=100 it seems to fail too often
WAIT_TIME = 3 # The docs recommend 3 seconds between queries
RETRY_WAIT = 8
RETRY_MAX = 20 # It fails a lot so retry a bunch
NUM_DUP_STOP = 30 # Number of dups to hit before determining we're done
BASE_URL = 'http://export.arxiv.org/api/query?'

# Pull Daily (arxiv updates 20:00 EST)
@periodic_task(
    run_every=crontab(),
    priority=2,
    options={'queue': f'{APP_ENV}_autopull_queue'}
)
def pull_papers(start=0):
    logger.info('Pulling Papers')

    Paper = apps.get_model('paper.Paper')
    Summary = apps.get_model('summary.Summary')
    Hub = apps.get_model('hub.Hub')

    # Namespaces don't quite work with the feedparser, so hack them in
    feedparser.namespaces._base.Namespace.supported_namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
    feedparser.namespaces._base.Namespace.supported_namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

    # Code Inspired from https://static.arxiv.org/static/arxiv.marxdown/0.1/help/api/examples/python_arXiv_parsing_example.txt
    # Original Author: Julius B. Lucks

    # All categories
    search_query = "+OR+".join(["cat:" + cat for cat in ARXIV_CATEGORIES])
    sortBy = "submittedDate"
    sortOrder = "descending"

    i = start
    num_retries = 0
    dups = 0
    while True:
        logger.info("Entries: %i - %i" % (i, i+RESULTS_PER_ITERATION))

        query = 'search_query=%s&start=%i&max_results=%i&sortBy=%s&sortOrder=%s&' % (
                search_query,
                i,
                RESULTS_PER_ITERATION,
                sortBy,
                sortOrder)

        with urllib.request.urlopen(BASE_URL+query) as url:
            response = url.read()
            feed = feedparser.parse(response)
            # If failed to fetch and we're not at the end retry until the limit
            if url.getcode() != 200:
                if num_retries < RETRY_MAX and i < int(feed.feed.opensearch_totalresults):
                    num_retries += 1
                    time.sleep(RETRY_WAIT)
                    continue
                else:
                    return

            if i == start:
                logger.info(f'Total results: {feed.feed.opensearch_totalresults}')
                logger.info(f'Last updated: {feed.feed.updated}')

            # If no results and we're at the end or we've hit the retry limit give up
            if len(feed.entries) == 0:
                if num_retries < RETRY_MAX and i < int(feed.feed.opensearch_totalresults):
                    num_retries += 1
                    time.sleep(RETRY_WAIT)
                    continue
                else:
                    return

            # Run through each entry, and print out information
            for entry in feed.entries:
                num_retries = 0
                try:
                    paper, created = Paper.objects.get_or_create(url=entry.id)
                    if created:
                        paper.alternate_ids = {'arxiv': entry.id.split('/abs/')[-1]}

                        paper.title = entry.title
                        paper.abstract = clean_abstract(entry.summary)
                        paper.paper_publish_date = entry.published.split('T')[0]
                        paper.raw_authors = {'main_author': entry.author}
                        paper.external_source = 'Arxiv'
                        paper.external_metadata = entry

                        try:
                            paper.raw_authors['main_author'] += ' (%s)' % entry.arxiv_affiliation
                        except AttributeError:
                            pass

                        try:
                            paper.raw_authors['other_authors'] = [author.name for author in entry.authors]
                        except AttributeError:
                            pass

                        for link in entry.links:
                            try:
                                if link.title == 'pdf':
                                    pdf_url = get_redirect_url(link.href)
                                    if pdf_url:
                                        paper.pdf_url = pdf_url
                                if link.title == 'doi':
                                    paper.doi = link.href.split('doi.org/')[-1]
                            except AttributeError:
                                pass

                        paper.save()

                        celery_calculate_paper_twitter_score.apply_async(
                            (paper.id,),
                            priority=5,
                            countdown=15
                        )

                        # If not published in the past week we're done
                        if Paper.objects.get(pk=paper.id).paper_publish_date < datetime.now().date() - timedelta(days=7):
                            return

                        # Arxiv Journal Ref
                        # try:
                            # journal_ref = entry.arxiv_journal_ref
                        # except AttributeError:
                            # journal_ref = 'No journal ref found'

                        # Arxiv Comment
                        # try:
                            # comment = entry.arxiv_comment
                        # except AttributeError:
                            # comment = 'No comment found'

                        # Arxiv Categories
                        # all_categories = [t['term'] for t in entry.tags]
                        try:
                            general_hub = get_general_hub_name(entry.arxiv_primary_category['term'])
                            if general_hub:
                                hub = Hub.objects.filter(name__iexact=general_hub).first()
                                if hub:
                                    paper.hubs.add(hub)

                            specific_hub = get_category_name(entry.arxiv_primary_category['term'])
                            if specific_hub:
                                shub = Hub.objects.filter(name__iexact=general_hub).first()
                                if shub:
                                    paper.hubs.add(shub)
                        except AttributeError:
                            pass
                    else:
                        # if we've reach the max dups then we're done
                        if dups > NUM_DUP_STOP:
                            return
                        else:
                            dups += 1
                except Exception as e:
                    sentry.log_error(e)

        # Rate limit
        time.sleep(WAIT_TIME)

        i += RESULTS_PER_ITERATION


# Crossref Download Constants
RESULTS_PER_ITERATION = 50
WAIT_TIME = 2
RETRY_WAIT = 8
RETRY_MAX = 20
NUM_DUP_STOP = 30

# Pull Daily
@periodic_task(
    run_every=crontab(minute=0, hour=12),
    priority=1,
    options={'queue': f'{APP_ENV}_autopull_queue'}
)
def pull_crossref_papers(start=0):
    logger.info('Pulling Crossref Papers')

    Paper = apps.get_model('paper.Paper')
    Hub = apps.get_model('hub.Hub')

    cr = Crossref()

    num_retries = 0 
    num_duplicates = 0

    offset = 0
    filters = {
        'type': 'journal-article',
        'from-pub-date': (datetime.now().date() - timedelta(days=1)).strftime('%Y-%m-%d'),
        'until-pub-date': datetime.now().date().strftime('%Y-%m-%d'),
    }

    while True:
        try:
            results = cr.works(
                filter=filters,
                limit=RESULTS_PER_ITERATION,
                sort='issued',
                order='desc',
                offset=offset,
            )
        except:
            if num_retries < RETRY_MAX:
                num_retries += 1
                time.sleep(RETRY_WAIT)
                continue
            else:
                return

        if results['message']['total-results'] == 0 or len(results['message']['items']) == 0:
            if num_retries < RETRY_MAX:
                num_retries += 1
                time.sleep(RETRY_WAIT)
                continue
            else:
                return

        for item in results['message']['items']:
            num_retries = 0
            try:
                paper, created = Paper.objects.get_or_create(doi=item['DOI'])
                if created:
                    paper.title = item['title'][0]
                    paper.paper_title = item['title'][0]
                    paper.slug = slugify(item['title'][0])
                    paper.doi = item['DOI']
                    paper.url = item['URL']
                    paper.paper_publish_date = get_crossref_issued_date(item)
                    paper.retrieved_from_external_source = True
                    paper.external_metadata = item
                    external_source = item.get('container-title', ['Crossref'])[0]
                    if type(external_source) is list:
                        external_source = external_source[0]

                    paper.external_source = external_source
                    paper.publication_type = item['type']
                    if 'abstract' in item:
                        paper.abstract = clean_abstract(item['abstract'])
                    else:
                        csl = get_csl_item(item['URL'])
                        abstract = csl.get('abstract', None)
                        if abstract:
                            paper.abstract = abstract
                        else:
                            # paper.delete()
                            paper.is_removed = True
                            continue
                    if 'author' in item:
                        paper.raw_authors = {}
                        for i, author in enumerate(item['author']):
                            author_name = []
                            if 'given' in author:
                                author_name.append(author['given'])
                            if 'family' in author:
                                author_name.append(author['family'])
                            author_name = ' '.join(author_name)
                            if author_name:
                                if i == 0:
                                    paper.raw_authors['main_author'] = author_name
                                else:
                                    if 'other_authors' not in paper.raw_authors:
                                        paper.raw_authors['other_authors'] = []
                                    else:
                                        paper.raw_authors['other_authors'].append(author_name)
                    if 'link' in item and item['link']:
                        pdf_url = get_redirect_url(item['link'][0]['URL'])
                        if check_url_contains_pdf(pdf_url):
                            paper.pdf_url = pdf_url
                    if 'subject' in item:
                        for subject_name in item['subject']:
                            hub = Hub.objects.filter(name__iexact=subject_name).first()
                            if hub:
                                paper.hubs.add(hub)
                    paper.save()
                    celery_calculate_paper_twitter_score.apply_async(
                        (paper.id,),
                        priority=5,
                        countdown=15
                    )
                else:
                    if num_duplicates > NUM_DUP_STOP:
                        return
                    num_duplicates += 1
            except Exception as e:
                sentry.log_error(e)

        offset += RESULTS_PER_ITERATION
        time.sleep(WAIT_TIME)
