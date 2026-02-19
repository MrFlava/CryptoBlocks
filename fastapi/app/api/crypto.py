from typing import Optional, List
from django.core.paginator import Paginator
from django.db.models import Q
from asgiref.sync import sync_to_async
from fastapi import HTTPException, Depends, Query
from app.models import User
from app.models.crypto import Currency, Provider, Block
from app.schemas.crypto import (
    BlockSchema,
    BlockListResponse,
    ProviderSchema,
    CurrencySchema
)
from app.dependencies.auth import get_current_user


class CryptoAPI:
    
    @classmethod
    async def get_blocks(
        cls,
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(10, ge=1, le=100, description="Items per page"),
        currency_name: Optional[str] = Query(None, description="Filter by currency name"),
        provider_id: Optional[int] = Query(None, description="Filter by provider ID"),
        current_user: User = Depends(get_current_user)
    ) -> BlockListResponse:
        """Get list of recorded blocks with filtering and pagination"""
        
        # Build query
        query = Block.objects.all()
        
        if currency_name:
            query = query.filter(currency__name__iexact=currency_name)
        
        if provider_id:
            query = query.filter(providers__id=provider_id)
        
        # Order by stored_at descending
        query = query.order_by('-stored_at')
        
        # Get total count
        total = await sync_to_async(query.count)()
        
        # Apply pagination using slicing
        offset = (page - 1) * page_size
        blocks_queryset = query[offset:offset + page_size]
        
        # Convert to schemas
        blocks = []
        async for block in blocks_queryset:
            # Get related objects
            await block.currency
            providers = [provider async for provider in block.providers.all()]
            
            block_schema = BlockSchema(
                id=block.id,
                currency=CurrencySchema(
                    id=block.currency.id,
                    name=block.currency.name
                ),
                block_number=block.block_number,
                providers=[
                    ProviderSchema(
                        id=provider.id,
                        name=provider.name,
                        api_key=provider.api_key
                    ) for provider in providers
                ],
                created_at=block.created_at,
                stored_at=block.stored_at
            )
            blocks.append(block_schema)
        
        return BlockListResponse(
            blocks=blocks,
            total=total,
            page=page,
            page_size=page_size
        )
    
    @classmethod
    async def get_block_by_currency_and_number(
        cls,
        currency_name: str,
        block_number: int,
        current_user: User = Depends(get_current_user)
    ) -> BlockSchema:
        """Get block by currency name and block number"""
        
        def _process_block():
            try:
                block = Block.objects.select_related('currency').prefetch_related('providers').get(
                    currency__name__iexact=currency_name,
                    block_number=block_number
                )
            except Block.DoesNotExist:
                raise HTTPException(status_code=404, detail="Block not found")
            
            # Get providers (synchronous)
            providers = list(block.providers.all())
            
            return BlockSchema(
                id=block.id,
                currency=CurrencySchema(
                    id=block.currency.id,
                    name=block.currency.name
                ),
                block_number=block.block_number,
                providers=[
                    ProviderSchema(
                        id=provider.id,
                        name=provider.name,
                        api_key=provider.api_key
                    ) for provider in providers
                ],
                created_at=block.created_at,
                stored_at=block.stored_at
            )
        
        return await sync_to_async(_process_block)()
    
    @classmethod
    async def get_block_by_id(
        cls,
        block_id: int,
        current_user: User = Depends(get_current_user)
    ) -> BlockSchema:
        """Get block by application ID"""
        
        def _process_block():
            try:
                block = Block.objects.select_related('currency').prefetch_related('providers').get(
                    id=block_id
                )
            except Block.DoesNotExist:
                raise HTTPException(status_code=404, detail="Block not found")
            
            # Get providers (synchronous)
            providers = list(block.providers.all())
            
            return BlockSchema(
                id=block.id,
                currency=CurrencySchema(
                    id=block.currency.id,
                    name=block.currency.name
                ),
                block_number=block.block_number,
                providers=[
                    ProviderSchema(
                        id=provider.id,
                        name=provider.name,
                        api_key=provider.api_key
                    ) for provider in providers
                ],
                created_at=block.created_at,
                stored_at=block.stored_at
            )
        
        return await sync_to_async(_process_block)()
    
    @classmethod
    async def get_providers(
        cls,
        current_user: User = Depends(get_current_user)
    ) -> List[ProviderSchema]:
        """Get list of available providers"""
        
        providers = []
        async for provider in Provider.objects.all():
            providers.append(ProviderSchema(
                id=provider.id,
                name=provider.name,
                api_key=provider.api_key
            ))
        
        return providers
    
    @classmethod
    async def get_currencies(
        cls,
        current_user: User = Depends(get_current_user)
    ) -> List[CurrencySchema]:
        """Get list of available currencies"""
        
        currencies = []
        async for currency in Currency.objects.all():
            currencies.append(CurrencySchema(
                id=currency.id,
                name=currency.name
            ))
        
        return currencies
