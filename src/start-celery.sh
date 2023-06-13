celery -A researchhub worker -Q cermine -l info --prefetch-multiplier=5 -P gevent --concurrency=5
