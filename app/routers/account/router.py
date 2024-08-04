from typing import Annotated, List
from json import loads
from fastapi import APIRouter, Depends, Response, HTTPException, Request, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, IntegrityError
from .utils import cloudinary_signature, cloudinary_verify
from .schemas import AccountLogin, AccountCreate, AccountResponse, AccountPictureSignature, AccountSearchItem, AccountUsernameAvailability, CheckAvailabilityParam
from ...utils import encode_auth_token
from ...models import AccountCRUD, InvalidPassword
from ...deps import get_db, get_current_user, CurrentUser

router = APIRouter()


@router.get("/me", response_model=AccountResponse)
def show(user: Annotated[CurrentUser, Depends(get_current_user)]):
    current_user, db = user
    return AccountCRUD(db).find(current_user.id)


@router.post(
        "/register",
        response_model=AccountResponse,
        status_code=status.HTTP_201_CREATED
)
def create(account: AccountCreate, db: Annotated[Session, Depends(get_db)]):
    account_crud = AccountCRUD(db)
    try:
        new_account = account_crud.create(account.name, account.username, account.email, account.password)
        account_crud.commit(new_account)
        return new_account
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e


@router.post("/login", response_model=AccountResponse)
def login(response: Response, account: AccountLogin, db: Annotated[Session, Depends(get_db)]):
    account_crud = AccountCRUD(db)
    try:
        user = account_crud.authenticate(account.identifier, account.password)
        response.headers['X-Token'] = encode_auth_token(user.id)
        return user
    except (NoResultFound, InvalidPassword) as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e


@router.get("/username-availability/{username}", response_model=AccountUsernameAvailability)
def check_availability(path_param: Annotated[CheckAvailabilityParam, Depends()], db: Annotated[Session, Depends(get_db)]):
    account_crud = AccountCRUD(db)

    return {
        "username": path_param.username,
        "available": account_crud.is_username_available(path_param.username),
    }


@router.get("/picture", response_model=AccountPictureSignature)
def sign_picture(user: Annotated[CurrentUser, Depends(get_current_user)]):
    return cloudinary_signature(user[0])


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


@router.get("/search/{query}", response_model=List[AccountSearchItem])
def search(query: str, user: Annotated[CurrentUser, Depends(get_current_user)]):
    current_user, db = user
    account_crud = AccountCRUD(db, current_user)
    return account_crud.search(query)
