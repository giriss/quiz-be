from datetime import datetime
from pydantic import BaseModel, EmailStr
from uuid import UUID


class AccountLogin(BaseModel):
    email: EmailStr
    password: str


class AccountCreate(AccountLogin):
    name: str


class AccountSearchItem(BaseModel):
    id: UUID
    name: str
    picture_id: UUID | None


class AccountResponse(AccountSearchItem):
    created_at: datetime


class AccountPictureSignature(BaseModel):
    api_key: str
    timestamp: int
    public_id: str
    signature: str
    cloud_name: str
