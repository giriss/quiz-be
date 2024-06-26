from datetime import datetime
from pydantic import BaseModel, EmailStr
from uuid import UUID


class EmailResponse(BaseModel):
    id: UUID
    address: EmailStr
    verified: bool
    primary: bool
    created_at: datetime
