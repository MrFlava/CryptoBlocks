from app.api import UserAPI
from app.dependencies.auth import get_current_user, get_current_admin_user
from app.models import User
from app.schemas import CreateUserSchema, ReadUserSchema

from fastapi import APIRouter, Depends, Request

user_router = APIRouter()


@user_router.get("/", response_model=ReadUserSchema)
async def get(request: Request, current_user: User = Depends(get_current_user)) -> User:
    return UserAPI.get(request, current_user)


@user_router.post(
    "/",
    response_model=ReadUserSchema,
)
async def create(request: Request, schema: CreateUserSchema) -> User:
    return await UserAPI.create(request, schema)


@user_router.post("/register", response_model=ReadUserSchema)
async def create_account_public(user_data: CreateUserSchema):
    """Create a new account (public endpoint - auto activates)"""
    return await UserAPI.create_account_public(user_data)


@user_router.post("/accounts", response_model=ReadUserSchema)
async def create_account_admin(
    user_data: CreateUserSchema, 
    current_user: User = Depends(get_current_admin_user)
):
    """Create a new account (admin only)"""
    return await UserAPI.create_account_admin(user_data, current_user)
