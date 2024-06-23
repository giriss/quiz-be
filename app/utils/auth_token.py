import os
import datetime
import jwt
from uuid import UUID

key = bytes.fromhex(os.getenv("SECRET_KEY_BASE"))


def encode(user_id: UUID) -> str:
    exp = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
    return jwt.encode({"user_id": str(user_id), "exp": exp}, key, "HS256")


def decode(token: str):
    return jwt.decode(token, key, "HS256")
