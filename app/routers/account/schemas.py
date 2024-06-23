from pydantic import BaseModel
from uuid import UUID


class AccountLogin(BaseModel):
    email: str
    password: str


class AccountCreate(AccountLogin):
    name: str


class AccountResponse(BaseModel):
    id: UUID
    name: str
    email: str
    email_verified: bool
