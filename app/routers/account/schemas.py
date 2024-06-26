from datetime import datetime
from pydantic import BaseModel, EmailStr
from uuid import UUID


class AccountLogin(BaseModel):
    email: EmailStr
    password: str


class AccountCreate(AccountLogin):
    name: str


class AccountResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime
