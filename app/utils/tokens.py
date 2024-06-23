import os
import datetime
import jwt
from uuid import UUID

key = bytes.fromhex(os.getenv("SECRET_KEY_BASE"))


def encode_auth_token(user_id: UUID | str) -> str:
    exp = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
    return jwt.encode({"user_id": str(user_id), "exp": exp}, key, "HS256")


def decode_auth_token(token: str) -> str:
    payload = jwt.decode(token, key, "HS256")
    return payload["user_id"]


def encode_verification_token(email: str) -> str:
    exp = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)
    return jwt.encode({"email": email, "exp": exp}, key, "HS256")


def decode_verification_token(token: str) -> str:
    payload = jwt.decode(token, key, "HS256")
    return payload["email"]
