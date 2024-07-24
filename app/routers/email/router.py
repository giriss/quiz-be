from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from ...models import Account, EmailCRUD
from ...deps import get_current_user, get_db, CurrentUser
from .schemas import EmailResponse, EmailCreate
from ...utils import decode_verification_token

router = APIRouter()


@router.get("", response_model=list[EmailResponse])
def index(user: Annotated[CurrentUser, Depends(get_current_user)]):
    return user[0].emails


@router.post("", response_model=EmailResponse, status_code=status.HTTP_201_CREATED)
def create(email: EmailCreate, user: Annotated[CurrentUser, Depends(get_current_user)]):
    current_user, db = user
    email_crud = EmailCRUD(db, current_user)
    created_email = email_crud.create(email.address)
    try:
        email_crud.commit(created_email)
        return created_email
    except IntegrityError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY) from e


@router.delete("/{address}", status_code=status.HTTP_204_NO_CONTENT)
def delete(address: str, user: Annotated[CurrentUser, Depends(get_current_user)]):
    current_user, db = user
    email_crud = EmailCRUD(db, current_user)
    try:
        email_crud.delete(address)
        email_crud.commit()
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e


@router.patch("/{address}/primary", status_code=status.HTTP_204_NO_CONTENT)
def set_primary(address: str, user: Annotated[CurrentUser, Depends(get_current_user)]):
    current_user, db = user
    email_crud = EmailCRUD(db, current_user)
    try:
        email = email_crud.make_primary(address)
        email_crud.commit(email)
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e


@router.patch("/verify/{token}", status_code=status.HTTP_204_NO_CONTENT)
def verify(token: str, db: Annotated[Session, Depends(get_db)]):
    email_crud = EmailCRUD(db)
    try:
        email = decode_verification_token(token)
        email_crud.verify(email)
        email_crud.commit()
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e
