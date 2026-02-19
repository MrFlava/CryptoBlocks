from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProviderSchema(BaseModel):
    id: int
    name: str
    api_key: str

    class Meta:
        model = "app.models.crypto.Provider"
        fields = "__all__"


class CurrencySchema(BaseModel):
    id: int
    name: str

    class Meta:
        model = "app.models.crypto.Currency"
        fields = "__all__"


class BlockSchema(BaseModel):
    id: int
    currency: CurrencySchema
    block_number: int
    providers: List[ProviderSchema]
    created_at: datetime
    stored_at: datetime

    class Meta:
        model = "app.models.crypto.Block"
        fields = "__all__"


class BlockListResponse(BaseModel):
    blocks: List[BlockSchema]
    total: int
    page: int
    page_size: int


class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = True


class UserResponseSchema(BaseModel):
    uuid: str
    username: str
    email: str
    is_active: bool
    is_admin: bool

    class Meta:
        model = "app.models.user.User"
        fields = ["uuid", "username", "email", "is_active", "is_admin"]
