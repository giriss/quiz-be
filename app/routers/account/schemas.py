from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, field_validator
from fastapi import Path

UsernamePath = Path(..., pattern=r'^[a-z0-9_.-]{3,25}$')


def validate_username(value: str):
    if not any(char.isalpha() for char in value):
        raise ValueError("Username must contain at least one letter")
    return value.lower()


class CheckAvailabilityParam(BaseModel):
    username: str = UsernamePath

    _validate_username = field_validator("username")(validate_username)


class AccountUsernameLogin(BaseModel):
    username: str = UsernamePath
    password: str

    _validate_username = field_validator("username")(validate_username)


class AccountEmailLogin(BaseModel):
    email: EmailStr
    password: str


class AccountCreate(BaseModel):
    email: EmailStr
    username: str = UsernamePath
    name: str
    password: str

    _validate_username = field_validator("username")(validate_username)


class AccountUsernameAvailability(BaseModel):
    username: str = UsernamePath
    available: bool

    _validate_username = field_validator("username")(validate_username)


class AccountSearchItem(BaseModel):
    id: UUID
    username: str = UsernamePath
    name: str
    picture_id: UUID | None

    _validate_username = field_validator("username")(validate_username)


class AccountResponse(AccountSearchItem):
    created_at: datetime


class AccountPictureSignature(BaseModel):
    api_key: str
    timestamp: int
    public_id: str
    signature: str
    cloud_name: str


AccountLogin = AccountEmailLogin | AccountUsernameLogin
