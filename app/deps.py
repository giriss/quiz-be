from typing import Annotated
from fastapi import Depends, HTTPException, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
from .utils import auth_token
from .models import AccountCRUD, Account
from .db import session_maker

http_bearer = HTTPBearer()


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
) -> Account:
    try:
        credentials = auth_token.decode(header.credentials)
        user_id = credentials["user_id"]
        response.headers['X-Token'] = auth_token.encode(user_id)
        return AccountCRUD(db).find(user_id)
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
