from typing import Annotated
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import bcrypt
import uuid
from .deps import get_db
from .models import Account
from .routers import router

app = FastAPI()


@app.get("/")
def index(db: Annotated[Session, Depends(get_db)]):
    pw_hash = bcrypt.hashpw(b"JavaScript6!", bcrypt.gensalt()).decode("ascii")
    new_acc = Account(id=uuid.uuid4(), name="Katha Kapadia", email="kiara@advani.in", password_hash=pw_hash)
    db.add(new_acc)
    db.commit()
    db.reset()
    accounts = db.query(Account).all()
    return {"ok": "ok", "accounts": accounts}

app.include_router(router)
