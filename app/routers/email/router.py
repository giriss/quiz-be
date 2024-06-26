from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from ...models import Account, EmailCRUD
from ...deps import get_current_user, get_db
from .schemas import EmailResponse
from ...utils import decode_verification_token

router = APIRouter()


@router.get("", response_model=list[EmailResponse])
def index(user: Annotated[Account, Depends(get_current_user)]):
    return user.emails


@router.get("/verify/{token}", status_code=status.HTTP_204_NO_CONTENT)
def verify(token: str, db: Annotated[Session, Depends(get_db)]):
    email_crud = EmailCRUD(db)
    try:
        email = decode_verification_token(token)
        email_crud.verify_account(email)
        email_crud.commit()
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e
