from typing import Annotated, Tuple
from fastapi import Depends, HTTPException, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
from .utils import decode_auth_token, encode_auth_token
from .models import AccountCRUD, Account
from .db import session_maker

http_bearer = HTTPBearer()
CurrentUser = Tuple[Account, Session]


def get_db():
    db = session_maker()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
        response: Response,
        header: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
        db: Annotated[Session, Depends(get_db)]
) -> CurrentUser:
    try:
        user_id = decode_auth_token(header.credentials)
        response.headers['X-Token'] = encode_auth_token(user_id)
        return AccountCRUD(db).find(user_id), db
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from e
