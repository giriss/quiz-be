from os import getenv
from .tokens import decode_auth_token, decode_verification_token, encode_auth_token, encode_verification_token

FASTAPI_ENV = getenv('FASTAPI_ENV') 
IS_DEV_ENV = FASTAPI_ENV == 'dev'
IS_TEST_ENV = FASTAPI_ENV == 'test'
IS_PROD_ENV = FASTAPI_ENV == 'prod'

__all__ = [
    "decode_auth_token",
    "decode_verification_token",
    "encode_auth_token",
    "encode_verification_token"
]
