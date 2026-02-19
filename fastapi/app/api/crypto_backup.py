from typing import Optional, List
from django.core.paginator import Paginator
from django.db.models import Q
from fastapi import HTTPException, Depends, Query
from app.models.crypto import Currency, Provider, Block
from app.schemas.crypto import (
    BlockSchema,
    BlockListResponse,
    ProviderSchema,
    CurrencySchema
)
from app.schemas import CreateUserSchema, ReadUserSchema
from app.models.user import User
from config.password import hash_password
from app.dependencies.auth import get_current_user, get_current_admin_user


class CryptoAPI:
    
    @classmethod
    async def create_account_public(
        cls,
        user_data: CreateUserSchema
    ) -> ReadUserSchema:
        """Create a new account (public endpoint - auto activates)"""
        
        # Check if email already exists
        existing_user = await User.objects.filter(email=user_data.email).afirst()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Check if username already exists
        existing_username = await User.objects.filter(username=user_data.username).afirst()
        if existing_username:
            raise HTTPException(status_code=400, detail="Username already taken")
        
        # Create user (always active for public registration)
        user = await User.objects.acreate(
            username=user_data.username,
            email=user_data.email,
            password=hash_password(user_data.password),
            is_active=True
        )
        
        return ReadUserSchema(
            uuid=user.uuid,
            username=user.username,
            email=user.email
        )
    
    @classmethod
    async def create_account(
        cls,
        user_data: CreateUserSchema,
        current_user: User = Depends(get_current_admin_user)
    ) -> ReadUserSchema:
        """Create a new account (admin only)"""
        
        # Check if email already exists
        existing_user = await User.objects.filter(email=user_data.email).afirst()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Check if username already exists
        existing_username = await User.objects.filter(username=user_data.username).afirst()
        if existing_username:
            raise HTTPException(status_code=400, detail="Username already taken")
        
        # Create user
        user = await User.objects.acreate(
            username=user_data.username,
            email=user_data.email,
            password=hash_password(user_data.password),
            is_active=user_data.is_active if hasattr(user_data, 'is_active') else True
        )
        
        return ReadUserSchema(
            uuid=user.uuid,
            username=user.username,
            email=user.email
        )
    #     page: int = Query(1, ge=1, description="Page number"),
    #     page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    #     currency_name: Optional[str] = Query(None, description="Filter by currency name"),
    #     provider_id: Optional[int] = Query(None, description="Filter by provider ID"),
    #     current_user: User = Depends(get_current_user)
    # ) -> BlockListResponse:
    #     """Get list of recorded blocks with filtering and pagination"""
    #
    #     # Build query
    #     query = Block.objects.all()
    #
    #     if currency_name:
    #         query = query.filter(currency__name__iexact=currency_name)
    #
    #     if provider_id:
    #         query = query.filter(providers__id=provider_id)
    #
    #     # Order by stored_at descending
    #     query = query.order_by('-stored_at')
    #
    #     # Paginate
    #     paginator = Paginator(query, page_size)
    #     page_obj = paginator.get_page(page)
    #
    #     # Convert to schemas
    #     blocks = []
    #     for block in page_obj.object_list:
    #         # Get related objects
    #         await block.acurrency
    #         providers = [provider async for provider in block.providers.all()]
    #
    #         block_schema = BlockSchema(
    #             id=block.id,
    #             currency=CurrencySchema(
    #                 id=block.currency.id,
    #                 name=block.currency.name
    #             ),
    #             block_number=block.block_number,
    #             providers=[
    #                 ProviderSchema(
    #                     id=provider.id,
    #                     name=provider.name,
    #                     api_key=provider.api_key
    #                 ) for provider in providers
    #             ],
    #             created_at=block.created_at,
    #             stored    # @classmethod
    #     # async def get_block_by_currency_and_number(
    #     #     cls,
    #     #     currency_name: str,
    #     #     block_number: int,
    #     #     current_user: User = Depends(get_current_user)
    #     # ) -> BlockSchema:
    #     #     """Get block by currency name and block number"""
    #     #
    #     #     try:
    #     #         block = await Block.objects.select_related('currency').prefetch_related('providers').get(
    #     #             currency__name__iexact=currency_name,
    #     #             block_number=block_number
    #     #         )
    #     #     except Block.DoesNotExist:
    #     #         raise HTTPException(status_code=404, detail="Block not found")
    #     #
    #     #     providers = [provider async for provider in block.providers.all()]
    #     #
    #     #     return BlockSchema(
    #     #         id=block.id,
    #     #         currency=CurrencySchema(
    #     #             id=block.currency.id,
    #     #             name=block.currency.name
    #     #         ),
    #     #         block_number=block.block_number,
    #     #         providers=[
    #     #             ProviderSchema(
    #     #                 id=provider.id,
    #     #                 name=provider.name,
    #     #                 api_key=provider.api_key
    #     #             ) for provider in providers
    #     #         ],
    #     #         created_at=block.created_at,
    #     #         stored_at=block.stored_at
    #     #     )
    #     #
    #     # @classmethod
    #     # async def get_block_by_id(
    #     #     cls,
    #     #     block_id: int,
    #     #     current_user: User = Depends(get_current_user)
    #     # ) -> BlockSchema:
    #     #     """Get block by application ID"""
    #     #
    #     #     try:
    #     #         block = await Block.objects.select_related('currency').prefetch_related('providers').get(
    #     #             id=block_id
    #     #         )
    #     #     except Block.DoesNotExist:
    #     #         raise HTTPException(status_code=404, detail="Block not found")
    #     #
    #     #     providers = [provider async for provider in block.providers.all()]
    #     #
    #     #     return BlockSchema(
    #     #         id=block.id,
    #     #         currency=CurrencySchema(
    #     #             id=block.currency.id,
    #     #             name=block.currency.name
    #     #         ),
    #     #         block_number=block.block_number,
    #     #         providers=[
    #     #             ProviderSchema(
    #     #                 id=provider.id,
    #     #                 name=provider.name,
    #     #                 api_key=provider.api_key
    #     #             ) for provider in providers
    #     #         ],
    #     #         created_at=block.created_at,
    #     #         stored_at=block.stored_at
    #     #     )
    #     #
    #     # @classmethod
    #     # async def get_providers(
    #     #     cls,
    #     #     current_user: User = Depends(get_current_user)
    #     # ) -> List[ProviderSchema]:
    #     #     """Get list of available providers"""
    #     #
    #     #     providers = []
    #     #     async for provider in Provider.objects.all():
    #     #         providers.append(ProviderSchema(
    #     #             id=provider.id,
    #     #             name=provider.name,
    #     #             api_key=provider.api_key
    #     #         ))
    #     #
    #     #     return providers
    #     #
    #     # @classmethod
    #     # async def get_currencies(
    #     #     cls,
    #     #     current_user: User = Depends(get_current_user)
    #     # ) -> List[CurrencySchema]:
    #     #     """Get list of available currencies"""
    #     #
    #     #     currencies = []
    #     #     async for currency in Currency.objects.all():
    #     #         currencies.append(CurrencySchema(
    #     #             id=currency.id,
    #     #             name=currency.name
    #     #         ))
    #     #
    #     #     return currencies_at=block.stored_at
    #         )
    #         blocks.append(block_schema)
    #
    #     return BlockListResponse(
    #         blocks=blocks,
    #         total=paginator.count,
    #         page=page,
    #         page_size=page_size
    #     )
    #

