from fastapi import status
from sqlalchemy.orm import Session
from app.models import Account
from app.utils import encode_verification_token
from ... import client


def test_verify(unverified_user: Account, db_session: Session):
    email_token = encode_verification_token(unverified_user.emails[0].address)
    assert not unverified_user.emails[0].verified
    response = client.get(f"/accounts/emails/verify/{email_token}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db_session.refresh(unverified_user)
    assert unverified_user.emails[0].verified
