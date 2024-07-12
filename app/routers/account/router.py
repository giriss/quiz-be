from typing import Annotated
from json import loads
from fastapi import APIRouter, Depends, Response, HTTPException, Request, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, IntegrityError
from .utils import cloudinary_signature, cloudinary_verify
from .schemas import AccountLogin, AccountCreate, AccountResponse, AccountPictureSignature
from ...utils import encode_auth_token
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
        new_account = account_crud.create(account.name, account.email, account.password)
        account_crud.commit(new_account)
        return new_account
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e


@router.post("/login", response_model=AccountResponse)
def login(response: Response, account: AccountLogin, db: Annotated[Session, Depends(get_db)]):
    account_crud = AccountCRUD(db)
    try:
        user = account_crud.authenticate(account.email, account.password)
        response.headers['X-Token'] = encode_auth_token(user.id)
        return user
    except (NoResultFound, InvalidPassword) as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e


@router.get("/picture", response_model=AccountPictureSignature)
def sign_picture(user: Annotated[Account, Depends(get_current_user)]):
    return cloudinary_signature(user)


@router.post("/picture", status_code=status.HTTP_204_NO_CONTENT)
async def verify_picture(request: Request, db: Annotated[Session, Depends(get_db)]):
    signature = request.headers["x-cld-signature"]
    timestamp = request.headers["x-cld-timestamp"]
    raw_body = (await request.body()).decode()
    if not cloudinary_verify(signature, int(timestamp), raw_body):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    body = loads(raw_body)
    account_id, picture_id = body["public_id"].split("_")
    account_crud = AccountCRUD(db)
    account_crud.set_picture(account_id, picture_id)
    account_crud.commit()
