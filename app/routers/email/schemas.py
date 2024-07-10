from datetime import datetime
from pydantic import BaseModel, EmailStr


class EmailResponse(BaseModel):
    address: EmailStr
    verified: bool
    primary: bool
    created_at: datetime


class EmailCreate(BaseModel):
    address: EmailStr
