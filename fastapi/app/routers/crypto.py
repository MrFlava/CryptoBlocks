from fastapi import APIRouter, Depends, Query
from app.api.crypto import CryptoAPI
from app.models.user import User
from app.schemas.crypto import (
    BlockSchema,
    BlockListResponse,
    ProviderSchema,
    CurrencySchema
)
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1", tags=["crypto"])

# Block endpoints
@router.get("/blocks", response_model=BlockListResponse)
async def get_blocks(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    currency_name: str = Query(None, description="Filter by currency name"),
    provider_id: int = Query(None, description="Filter by provider ID"),
    current_user: User = Depends(get_current_user)
):
    """Get list of recorded blocks with filtering and pagination"""
    return await CryptoAPI.get_blocks(page, page_size, currency_name, provider_id, current_user)

@router.get("/blocks/by-currency/{currency_name}/{block_number}", response_model=BlockSchema)
async def get_block_by_currency_and_number(
    currency_name: str,
    block_number: int,
    current_user: User = Depends(get_current_user)
):
    """Get block by currency name and block number"""
    return await CryptoAPI.get_block_by_currency_and_number(currency_name, block_number, current_user)

@router.get("/blocks/{block_id}", response_model=BlockSchema)
async def get_block_by_id(
    block_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get block by application ID"""
    return await CryptoAPI.get_block_by_id(block_id, current_user)

# Reference data endpoints
@router.get("/providers", response_model=list[ProviderSchema])
async def get_providers(current_user: User = Depends(get_current_user)):
    """Get list of available providers"""
    return await CryptoAPI.get_providers(current_user)

@router.get("/currencies", response_model=list[CurrencySchema])
async def get_currencies(current_user: User = Depends(get_current_user)):
    """Get list of available currencies"""
    return await CryptoAPI.get_currencies(current_user)
