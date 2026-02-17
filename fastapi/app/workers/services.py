from django.utils import timezone
from app.models.crypto import Currency, Provider, Block

def store_block(data):
    currency, _ = Currency.objects.get_or_create(name="Ethereum")
    provider, _ = Provider.objects.get_or_create(name="Blockchair", defaults={"api_key": "N/A"})
    block_number = data.get("best_block_height")
    block_time = data.get("best_block_time")

    if not Block.objects.filter(currency=currency, block_number=block_number).exists():
        block = Block.objects.create(
            currency=currency,
            block_number=block_number,
            created_at=block_time,
            stored_at=timezone.now()
        )
        block.providers.add(provider)
