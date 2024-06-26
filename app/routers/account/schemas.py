from datetime import datetime
from pydantic import BaseModel, EmailStr
from uuid import UUID


class AccountLogin(BaseModel):
    email: EmailStr
    password: str


class AccountCreate(AccountLogin):
    name: str


class EmailResponse(BaseModel):
    id: UUID
    address: EmailStr
    verified: bool
    primary: bool
    created_at: datetime


class AccountResponse(BaseModel):
    id: UUID
    name: str
    emails: list[EmailResponse]
    created_at: datetime
