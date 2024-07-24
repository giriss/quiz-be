from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from .schemas import ConnectionCreate, ConnectionResponse
from ...deps import CurrentUser, get_current_user
from ...models import ConnectionCRUD

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ConnectionResponse)
def create(params: ConnectionCreate, user: Annotated[CurrentUser, Depends(get_current_user)]):
    current_user, db = user
    connection_crud = ConnectionCRUD(db, current_user)
    try:
        connection = connection_crud.create(params.responder_id)
        connection_crud.commit(connection)
        return connection
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY) from e


@router.get("", response_model=List[ConnectionResponse])
def index(user: Annotated[CurrentUser, Depends(get_current_user)]):
    current_user, db = user
    connection_crud = ConnectionCRUD(db, current_user)
    return connection_crud.list_all()
