from celery.schedules import crontab

CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"

CELERY_BEAT_SCHEDULE = {
    "fetch-ethereum-stats-every-minute": {
        "task": "app.workers.eth_fetcher.fetch_ethereum_stats", 
        "schedule": crontab(minute="*"),
    },
}

