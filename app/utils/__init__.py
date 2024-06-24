from os import getenv
from .tokens import decode_auth_token, decode_verification_token, encode_auth_token, encode_verification_token

IS_DEV_ENV = getenv('FASTAPI_ENV') == 'dev'

__all__ = [
    "decode_auth_token",
    "decode_verification_token",
    "encode_auth_token",
    "encode_verification_token",
    "IS_DEV_ENV"
]
