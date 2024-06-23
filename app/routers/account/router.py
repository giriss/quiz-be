from typing import Annotated
from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, IntegrityError
from .schemas import AccountLogin, AccountCreate, AccountResponse
from ...utils import auth_token
from ...models import AccountCRUD, Account, InvalidPassword
from ...deps import get_db, get_current_user

router = APIRouter()


@router.get("/me", response_model=AccountResponse)
def show(db: Annotated[Session, Depends(get_db)], user: Annotated[Account, Depends(get_current_user)]):
    return AccountCRUD(db).find(user.id)


@router.post(
        "/register",
        response_model=AccountResponse,
        status_code=status.HTTP_201_CREATED
)
def create(account: AccountCreate, db: Annotated[Session, Depends(get_db)]):
    account_crud = AccountCRUD(db)
    try:
        return account_crud.create(account.name, account.email, account.password)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@router.post("/login", response_model=AccountResponse)
def login(response: Response, account: AccountLogin, db: Annotated[Session, Depends(get_db)]):
    account_crud = AccountCRUD(db)
    try:
        user = account_crud.authenticate(account.email, account.password)
        response.headers['X-Token'] = auth_token.encode(user.id)
        return user
    except (NoResultFound, InvalidPassword):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
