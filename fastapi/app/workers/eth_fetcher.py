from celery import shared_task
import requests

from .services import store_block

@shared_task
def fetch_ethereum_stats():
    response = requests.get("https://api.blockchair.com/ethereum/stats")
    if response.status_code == 200:
        data = response.json().get("data", {})
        store_block(data)
