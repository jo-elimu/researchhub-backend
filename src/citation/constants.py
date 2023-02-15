# from .schema import (
#     ACCESSED_SCHEMA_FIELDS,
#     BOOKS_AND_PERIODICALS_SCHEMA_FIELDS,
#     GENERAL_SCHEMA_FIELDS,
#     IMAGES_ARTWORK_MAPS_SCHEMA_FIELDS,
#     LEGAL_CASES_SCHEMA_FIELDS,
#     LEGISLATION_AND_HEARINGS_SCHEMA,
#     PATENTS_SCHEMA_FIELDS,
#     PRESENTATION_AND_PERFORMANCES_SCHEMA_FIELDS,
#     RECORDING_AND_BROADCAST_SCHEMA_FIELDS,
#     WEBSITE_SCHEMA_FIELDS,
# )

ARTWORK = "ARTWORK"
AUDIO_RECORDING = "AUDIO_RECORDING"
BILL = "BILL"
BLOG_POST = "BLOG_POST"
BOOK = "BOOK"
BOOK_SECTION = "BOOK_SECTION"
CASE = "CASE"
CONFERENCE_PAPER = "CONFERENCE_PAPER"
DICTIONARY_ENTRY = "DICTIONARY_ENTRY"
DOCUMENT = "DOCUMENT"
EMAIL = "EMAIL"
ENCYCLOPEDIA_ARTICLE = "ENCYCLOPEDIA_ARTICLE"
FILM = "FILM"
FORUM_POST = "FORUM_POST"
HEARING = "HEARING"
INSTANT_MESSAGE = "INSTANT_MESSAGE"
INTERVIEW = "INTERVIEW"
JOURNAL_ARTICLE = "JOURNAL_ARTICLE"
LETTER = "LETTER"
MAGAZINE_ARTICLE = "MAGAZINE_ARTICLE"
MANUSCRIPT = "MANUSCRIPT"
MAP = "MAP"
NEWSPAPER_ARTICLE = "NEWSPAPER_ARTICLE"
PATENT = "PATENT"
PODCAST = "PODCAST"
PREPRINT = "PREPRINT"
PRESENTATION = "PRESENTATION"
RADIO_BROADCAST = "RADIO_BROADCAST"
REPORT = "REPORT"
SOFTWARE = "SOFTWARE"
STATUTE = "STATUTE"
THESIS = "THESIS"
TV_BROADCAST = "TV_BROADCAST"
VIDEO_RECORDING = "VIDEO_RECORDING"
WEB_PAGE = "WEB_PAGE"

CITATION_TYPE_CHOICES = (
    (ARTWORK, ARTWORK),
    (AUDIO_RECORDING, AUDIO_RECORDING),
    (BILL, BILL),
    (BLOG_POST, BLOG_POST),
    (BOOK, BOOK),
    (BOOK_SECTION, BOOK_SECTION),
    (CASE, CASE),
    (CONFERENCE_PAPER, CONFERENCE_PAPER),
    (DICTIONARY_ENTRY, DICTIONARY_ENTRY),
    (DOCUMENT, DOCUMENT),
    (EMAIL, EMAIL),
    (ENCYCLOPEDIA_ARTICLE, ENCYCLOPEDIA_ARTICLE),
    (FILM, FILM),
    (FORUM_POST, FORUM_POST),
    (HEARING, HEARING),
    (INSTANT_MESSAGE, INSTANT_MESSAGE),
    (INTERVIEW, INTERVIEW),
    (JOURNAL_ARTICLE, JOURNAL_ARTICLE),
    (LETTER, LETTER),
    (MAGAZINE_ARTICLE, MAGAZINE_ARTICLE),
    (MANUSCRIPT, MANUSCRIPT),
    (MAP, MAP),
    (NEWSPAPER_ARTICLE, NEWSPAPER_ARTICLE),
    (PATENT, PATENT),
    (PODCAST, PODCAST),
    (PREPRINT, PREPRINT),
    (PRESENTATION, PRESENTATION),
    (RADIO_BROADCAST, RADIO_BROADCAST),
    (REPORT, REPORT),
    (SOFTWARE, SOFTWARE),
    (STATUTE, STATUTE),
    (THESIS, THESIS),
    (TV_BROADCAST, TV_BROADCAST),
    (VIDEO_RECORDING, VIDEO_RECORDING),
    (WEB_PAGE, WEB_PAGE),
)

# OLD_CITATION_TYPE_FIELDS = {
#     "ARTWORK_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         *IMAGES_ARTWORK_MAPS_SCHEMA_FIELDS,
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "AUDIO_RECORDING_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         *RECORDING_AND_BROADCAST_SCHEMA_FIELDS,
#         *BOOKS_AND_PERIODICALS_SCHEMA_FIELDS,
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "BILL_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         *LEGISLATION_AND_HEARINGS_SCHEMA,
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "BLOG_POST_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         *WEBSITE_SCHEMA_FIELDS,
#         "blog_title",
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "BOOK_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         *BOOKS_AND_PERIODICALS_SCHEMA_FIELDS,
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "BOOK_SECTION_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         *BOOKS_AND_PERIODICALS_SCHEMA_FIELDS,
#         "book_title",
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "CASE_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         *LEGAL_CASES_SCHEMA_FIELDS,
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "CONFERENCE_PAPER_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         *PRESENTATION_AND_PERFORMANCES_SCHEMA_FIELDS,
#         "proceedings_title",
#         *BOOKS_AND_PERIODICALS_SCHEMA_FIELDS,
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "DICTIONARY_ENTRY_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         BOOKS_AND_PERIODICALS_SCHEMA_FIELDS,
#         "dictionary_title",
#         ACCESSED_SCHEMA_FIELDS,
#     ],
#     "DOCUMENT_FIELDS": [*GENERAL_SCHEMA_FIELDS, "publisher", *ACCESSED_SCHEMA_FIELDS],
#     "EMAIL_FIELDS": [*GENERAL_SCHEMA_FIELDS, *ACCESSED_SCHEMA_FIELDS],
#     "ENCYCLOPEDIA_ARTICLE_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         "encyclopedia_title",
#         *BOOKS_AND_PERIODICALS_SCHEMA_FIELDS,
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "FILM_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         *RECORDING_AND_BROADCAST_SCHEMA_FIELDS,
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "FORUM_POST_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         *WEBSITE_SCHEMA_FIELDS,
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "HEARING_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         *BOOKS_AND_PERIODICALS_SCHEMA_FIELDS,
#         "number_of_volumes",
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "INSTANT_MESSAGE_FIELDS": [*GENERAL_SCHEMA_FIELDS, *ACCESSED_SCHEMA_FIELDS],
#     "INTERVIEW_FIELDS": [*GENERAL_SCHEMA_FIELDS, "medium", *ACCESSED_SCHEMA_FIELDS],
#     "JOURNAL_ARTICLE_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         *BOOKS_AND_PERIODICALS_SCHEMA_FIELDS,
#         "series_text",
#         "doi",
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "LETTER_FIELDS": [*GENERAL_SCHEMA_FIELDS, *ACCESSED_SCHEMA_FIELDS],
#     "MAGAZINE_ARTICLE_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         *BOOKS_AND_PERIODICALS_SCHEMA_FIELDS,
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "MANUSCRIPT_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         "place",
#         "number_of_pages",
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "MAP_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         *IMAGES_ARTWORK_MAPS_SCHEMA_FIELDS,
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "NEWSPAPER_ARTICLE_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         *BOOKS_AND_PERIODICALS_SCHEMA_FIELDS,
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "PATENT_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         *PATENTS_SCHEMA_FIELDS,
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "PODCAST_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         "series_title",
#         "episode_number",
#         *RECORDING_AND_BROADCAST_SCHEMA_FIELDS,
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "PREPRINT_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#     ],
#     "PRESENTATION_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#         "meeting_name",
#         *PRESENTATION_AND_PERFORMANCES_SCHEMA_FIELDS,
#         *ACCESSED_SCHEMA_FIELDS,
#     ],
#     "RADIO_BROADCAST_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#     ],
#     "REPORT_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#     ],
#     "SOFTWARE_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#     ],
#     "STATUTE_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#     ],
#     "THESIS_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#     ],
#     "TV_BROADCAST_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#     ],
#     "VIDEO_RECORDING_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#     ],
#     "WEB_PAGE_FIELDS": [
#         *GENERAL_SCHEMA_FIELDS,
#     ],
# }

CITATION_TYPE_FIELDS = {
    # "annotation": [],
    ARTWORK: [
        "title",
        "abstract_note",
        "artwork_medium",
        "artwork_size",
        "date",
        "language",
        "short_title",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "url",
        "access_date",
        "rights",
        "extra",
    ],
    # ATTACHMENT: ["title", "access_date", "url"],
    AUDIO_RECORDING: [
        "title",
        "abstract_note",
        "audio_recording_format",
        "series_title",
        "volume",
        "number_of_volumes",
        "place",
        "label",
        "date",
        "running_time",
        "language",
        "ISBN",
        "short_title",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "url",
        "access_date",
        "rights",
        "extra",
    ],
    BILL: [
        "title",
        "abstract_note",
        "bill_number",
        "code",
        "code_volume",
        "section",
        "code_pages",
        "legislative_body",
        "session",
        "history",
        "date",
        "language",
        "url",
        "access_date",
        "short_title",
        "rights",
        "extra",
    ],
    BLOG_POST: [
        "title",
        "abstract_note",
        "blog_title",
        "website_type",
        "date",
        "url",
        "access_date",
        "language",
        "short_title",
        "rights",
        "extra",
    ],
    BOOK: [
        "title",
        "abstract_note",
        "series",
        "series_number",
        "volume",
        "number_of_volumes",
        "edition",
        "place",
        "publisher",
        "date",
        "num_pages",
        "language",
        "ISBN",
        "short_title",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    BOOK_SECTION: [
        "title",
        "abstract_note",
        "book_title",
        "series",
        "series_number",
        "volume",
        "number_of_volumes",
        "edition",
        "place",
        "publisher",
        "date",
        "pages",
        "language",
        "ISBN",
        "short_title",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    CASE: [
        "case_name",
        "abstract_note",
        "court",
        "date_decided",
        "docket_number",
        "reporter",
        "reporter_volume",
        "first_page",
        "history",
        "language",
        "short_title",
        "url",
        "access_date",
        "rights",
        "extra",
    ],
    SOFTWARE: [
        "title",
        "abstract_note",
        "series_title",
        "version_number",
        "date",
        "system",
        "place",
        "company",
        "programming_language",
        "ISBN",
        "short_title",
        "url",
        "rights",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "access_date",
        "extra",
    ],
    CONFERENCE_PAPER: [
        "title",
        "abstract_note",
        "date",
        "proceedings_title",
        "conference_name",
        "place",
        "publisher",
        "volume",
        "pages",
        "series",
        "language",
        "DOI",
        "ISBN",
        "short_title",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    DICTIONARY_ENTRY: [
        "title",
        "abstract_note",
        "dictionary_title",
        "series",
        "series_number",
        "volume",
        "number_of_volumes",
        "edition",
        "place",
        "publisher",
        "date",
        "pages",
        "language",
        "ISBN",
        "short_title",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    DOCUMENT: [
        "title",
        "abstract_note",
        "publisher",
        "date",
        "language",
        "short_title",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    EMAIL: [
        "subject",
        "abstract_note",
        "date",
        "short_title",
        "url",
        "access_date",
        "language",
        "rights",
        "extra",
    ],
    ENCYCLOPEDIA_ARTICLE: [
        "title",
        "abstract_note",
        "encyclopedia_title",
        "series",
        "series_number",
        "volume",
        "number_of_volumes",
        "edition",
        "place",
        "publisher",
        "date",
        "pages",
        "ISBN",
        "short_title",
        "url",
        "access_date",
        "language",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    FILM: [
        "title",
        "abstract_note",
        "distributor",
        "date",
        "genre",
        "video_recording_format",
        "running_time",
        "language",
        "short_title",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    FORUM_POST: [
        "title",
        "abstract_note",
        "forum_title",
        "post_type",
        "date",
        "language",
        "short_title",
        "url",
        "access_date",
        "rights",
        "extra",
    ],
    HEARING: [
        "title",
        "abstract_note",
        "committee",
        "place",
        "publisher",
        "number_of_volumes",
        "document_number",
        "pages",
        "legislative_body",
        "session",
        "history",
        "date",
        "language",
        "short_title",
        "url",
        "access_date",
        "rights",
        "extra",
    ],
    INSTANT_MESSAGE: [
        "title",
        "abstract_note",
        "date",
        "language",
        "short_title",
        "url",
        "access_date",
        "rights",
        "extra",
    ],
    INTERVIEW: [
        "title",
        "abstract_note",
        "date",
        "interview_medium",
        "language",
        "short_title",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    JOURNAL_ARTICLE: [
        "title",
        "abstract_note",
        "publication_title",
        "volume",
        "issue",
        "pages",
        "date",
        "series",
        "series_title",
        "series_text",
        "journal_abbreviation",
        "language",
        "DOI",
        "ISSN",
        "short_title",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    LETTER: [
        "title",
        "abstract_note",
        "letter_type",
        "date",
        "language",
        "short_title",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    MAGAZINE_ARTICLE: [
        "title",
        "abstract_note",
        "publication_title",
        "volume",
        "issue",
        "date",
        "pages",
        "language",
        "ISSN",
        "short_title",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    MANUSCRIPT: [
        "title",
        "abstract_note",
        "manuscript_type",
        "place",
        "date",
        "num_pages",
        "language",
        "short_title",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    MAP: [
        "title",
        "abstract_note",
        "map_type",
        "scale",
        "series_title",
        "edition",
        "place",
        "publisher",
        "date",
        "language",
        "ISBN",
        "short_title",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    NEWSPAPER_ARTICLE: [
        "title",
        "abstract_note",
        "publication_title",
        "place",
        "edition",
        "date",
        "section",
        "pages",
        "language",
        "short_title",
        "ISSN",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    # NOTE: [],
    PATENT: [
        "title",
        "abstract_note",
        "place",
        "country",
        "assignee",
        "issuing_authority",
        "patent_number",
        "filing_date",
        "pages",
        "application_number",
        "priority_numbers",
        "issue_date",
        "references",
        "legal_status",
        "language",
        "short_title",
        "url",
        "access_date",
        "rights",
        "extra",
    ],
    PODCAST: [
        "title",
        "abstract_note",
        "series_title",
        "episode_number",
        "audio_file_type",
        "running_time",
        "url",
        "access_date",
        "language",
        "short_title",
        "rights",
        "extra",
    ],
    PREPRINT: [
        "title",
        "abstract_note",
        "genre",
        "repository",
        "archive_ID",
        "place",
        "date",
        "series",
        "series_number",
        "DOI",
        "citation_key",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "short_title",
        "language",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    PRESENTATION: [
        "title",
        "abstract_note",
        "presentation_type",
        "date",
        "place",
        "meeting_name",
        "url",
        "access_date",
        "language",
        "short_title",
        "rights",
        "extra",
    ],
    RADIO_BROADCAST: [
        "title",
        "abstract_note",
        "program_title",
        "episode_number",
        "audio_recording_format",
        "place",
        "network",
        "date",
        "running_time",
        "language",
        "short_title",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    REPORT: [
        "title",
        "abstract_note",
        "report_number",
        "report_type",
        "series_title",
        "place",
        "institution",
        "date",
        "pages",
        "language",
        "short_title",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    STATUTE: [
        "name_of_act",
        "abstract_note",
        "code",
        "code_number",
        "public_law_number",
        "date_enacted",
        "pages",
        "section",
        "session",
        "history",
        "language",
        "short_title",
        "url",
        "access_date",
        "rights",
        "extra",
    ],
    THESIS: [
        "title",
        "abstract_note",
        "thesis_type",
        "university",
        "place",
        "date",
        "num_pages",
        "language",
        "short_title",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    TV_BROADCAST: [
        "title",
        "abstract_note",
        "program_title",
        "episode_number",
        "video_recording_format",
        "place",
        "network",
        "date",
        "running_time",
        "language",
        "short_title",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    VIDEO_RECORDING: [
        "title",
        "abstract_note",
        "video_recording_format",
        "series_title",
        "volume",
        "number_of_volumes",
        "place",
        "studio",
        "date",
        "running_time",
        "language",
        "ISBN",
        "short_title",
        "url",
        "access_date",
        "archive",
        "archive_location",
        "library_catalog",
        "call_number",
        "rights",
        "extra",
    ],
    WEB_PAGE: [
        "title",
        "abstract_note",
        "website_title",
        "website_type",
        "date",
        "short_title",
        "url",
        "access_date",
        "language",
        "rights",
        "extra",
    ],
}

FIELD_NAME_ALT = {
    "artwork_medium": "medium",
    "audio_recording_format": "medium",
    "label": "publisher",
    "bill_number": "number",
    "code_volume": "volume",
    "code_pages": "pages",
    "blog_title": "publication_title",
    "website_type": "type",
    "book_title": "publication_title",
    "case_name": "title",
    "date_decided": "date",
    "docket_number": "number",
    "reporter_volume": "volume",
    "first_page": "pages",
    "company": "publisher",
    "proceedings_title": "publication_title",
    "dictionary_title": "publication_title",
    "subject": "title",
    "encyclopedia_title": "publication_title",
    "distributor": "publisher",
    "genre": "type",
    "video_recording_format": "medium",
    "forum_title": "publication_title",
    "post_type": "type",
    "document_number": "number",
    "interview_medium": "medium",
    "letter_type": "type",
    "manuscript_type": "type",
    "map_type": "type",
    "patent_number": "number",
    "issue_date": "date",
    "episode_number": "number",
    "audio_file_type": "medium",
    "repository": "publisher",
    "archive_ID": "number",
    "presentation_type": "type",
    "program_title": "publication_title",
    "network": "publisher",
    "report_number": "number",
    "report_type": "type",
    "institution": "publisher",
    "name_of_act": "title",
    "public_law_number": "number",
    "date_enacted": "date",
    "thesis_type": "type",
    "university": "publisher",
    "studio": "publisher",
    "website_title": "publication_title",
}

CREATOR_TYPES = {
    # "annotation": [],
    ARTWORK: ["artist", "contributor"],
    # ATTACHMENT: [],
    AUDIO_RECORDING: ["performer", "contributor", "composer", "words_by"],
    BILL: ["sponsor", "cosponsor", "contributor"],
    BLOG_POST: ["author", "commenter", "contributor"],
    BOOK: ["author", "contributor", "editor", "translator", "series_editor"],
    BOOK_SECTION: [
        "author",
        "contributor",
        "editor",
        "book_author",
        "translator",
        "series_editor",
    ],
    CASE: ["author", "counsel", "contributor"],
    SOFTWARE: ["programmer", "contributor"],
    CONFERENCE_PAPER: [
        "author",
        "contributor",
        "editor",
        "translator",
        "series_editor",
    ],
    DICTIONARY_ENTRY: [
        "author",
        "contributor",
        "editor",
        "translator",
        "series_editor",
    ],
    DOCUMENT: ["author", "contributor", "editor", "translator", "reviewed_author"],
    EMAIL: ["author", "contributor", "recipient"],
    ENCYCLOPEDIA_ARTICLE: [
        "author",
        "contributor",
        "editor",
        "translator",
        "series_editor",
    ],
    FILM: ["director", "contributor", "scriptwriter", "producer"],
    FORUM_POST: ["author", "contributor"],
    HEARING: ["contributor"],
    INSTANT_MESSAGE: ["author", "contributor", "recipient"],
    INTERVIEW: ["interviewee", "contributor", "interviewer", "translator"],
    JOURNAL_ARTICLE: [
        "author",
        "contributor",
        "editor",
        "translator",
        "reviewed_author",
    ],
    LETTER: ["author", "contributor", "recipient"],
    MAGAZINE_ARTICLE: ["author", "contributor", "translator", "reviewed_author"],
    MANUSCRIPT: ["author", "contributor", "translator"],
    MAP: ["cartographer", "contributor", "series_editor"],
    NEWSPAPER_ARTICLE: ["author", "contributor", "translator", "reviewed_author"],
    # NOTE: [],
    PATENT: ["inventor", "attorney_agent", "contributor"],
    PODCAST: ["podcaster", "contributor", "guest"],
    PREPRINT: ["author", "contributor", "editor", "translator", "reviewed_author"],
    PRESENTATION: ["presenter", "contributor"],
    RADIO_BROADCAST: [
        "director",
        "scriptwriter",
        "producer",
        "cast_member",
        "contributor",
        "guest",
    ],
    REPORT: ["author", "contributor", "translator", "series_editor"],
    STATUTE: ["author", "contributor"],
    THESIS: ["author", "contributor"],
    TV_BROADCAST: [
        "director",
        "scriptwriter",
        "producer",
        "cast_member",
        "contributor",
        "guest",
    ],
    VIDEO_RECORDING: [
        "director",
        "scriptwriter",
        "producer",
        "cast_member",
        "contributor",
    ],
    WEB_PAGE: ["author", "contributor", "translator"],
}
