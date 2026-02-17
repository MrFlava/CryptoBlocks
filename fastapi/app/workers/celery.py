import os
import django
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

app = Celery("fastapi_django_template")
app.config_from_object("app.workers.settings", namespace="CELERY")

# Import tasks explicitly to ensure registration
from app.workers.eth_fetcher import fetch_ethereum_stats

print("Registered tasks:", list(app.tasks.keys()))
