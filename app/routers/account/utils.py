from os import getenv
from datetime import datetime
from uuid import uuid4
from urllib.parse import urlparse
from cloudinary.utils import api_sign_request, verify_notification_signature
from .schemas import AccountPictureSignature
from ...models import Account


def cloudinary_signature(user: Account) -> AccountPictureSignature:
    cloudinary_credentials = urlparse(getenv("CLOUDINARY_URL"))
    timestamp = int(datetime.now().timestamp())
    public_id = f"{user.id}_{uuid4()}"
    signature = api_sign_request(
        {"public_id": public_id, "timestamp": timestamp},
        cloudinary_credentials.password
    )
    return AccountPictureSignature(
        api_key=cloudinary_credentials.username,
        timestamp=timestamp,
        cloud_name=cloudinary_credentials.hostname,
        public_id=public_id,
        signature=signature
    )


def cloudinary_verify(signature: str, timestamp: int, body: str) -> bool:
    return verify_notification_signature(body, timestamp, signature)
