import os
from typing import List

from celery.schedules import crontab

from .base import *  # noqa

DEBUG = True

ALLOWED_HOSTS: List[str] = ["*"]


CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"

CELERY_BEAT_SCHEDULE = {
    "fetch-ethereum-stats-every-minute": {
        "task": "workers.eth_fetcher.fetch_ethereum_stats", "schedule": crontab(minute="*"),
    },
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql_psycopg2"),
        "NAME": os.getenv("DB_NAME", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.getenv("DB_USER", "user"),
        "PASSWORD": os.getenv("DB_PASSWORD", "password"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}
