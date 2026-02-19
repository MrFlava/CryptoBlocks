from logging import getLogger

from app.models import User
from app.schemas import CreateUserSchema, ReadUserSchema
from asgiref.sync import sync_to_async
from config.password import hash_password
from app.dependencies.auth import get_current_admin_user

from fastapi import HTTPException, Request, Depends

logger = getLogger(__name__)


class UserAPI:
    @classmethod
    def get(cls, request: Request, current_user: User) -> User:
        return current_user

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
    async def create(cls, request: Request, schema: CreateUserSchema) -> User:
        user = await User.objects.filter(email=schema.email).afirst()
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")
        schema.password = hash_password(schema.password)
        return await sync_to_async(User.objects.create)(**schema.dict())
    
    @classmethod
    async def create_account_admin(
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
