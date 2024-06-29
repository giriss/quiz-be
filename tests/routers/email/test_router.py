from fastapi import status
from sqlalchemy.orm import Session
from app.models import Account, Email, EmailCRUD
from app.utils import encode_verification_token
from ... import client


def test_index(verified_user_with_token: tuple[Account, str]):
    user, auth_token = verified_user_with_token
    response = client.get("/accounts/emails", headers={"Authorization": f"Bearer {auth_token}"})
    body = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(body) == 1
    assert body[0]["id"] == str(user.emails[0].id)
    assert body[0]["address"] == user.emails[0].address
    assert body[0]["verified"]
    assert body[0]["primary"]


def test_verify(unverified_user: Account, db_session: Session):
    email_token = encode_verification_token(unverified_user.emails[0].address)
    assert not unverified_user.emails[0].verified
    response = client.patch(f"/accounts/emails/verify/{email_token}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db_session.refresh(unverified_user)
    assert unverified_user.emails[0].verified


def test_verify_with_invalid_token(unverified_user: Account):
    email_token = f"{encode_verification_token(unverified_user.emails[0].address)}a"
    response = client.patch(f"/accounts/emails/verify/{email_token}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create(verified_user_with_token: tuple[Account, str], db_session: Session):
    assert db_session.query(Email).count() == 1

    auth_token = verified_user_with_token[1]
    response = client.post(
        "/accounts/emails",
        json={"address": "gopaul0510@gmail.com"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    body = response.json()

    assert db_session.query(Email).count() == 2
    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(body["id"], str)
    assert body["address"] == "gopaul0510@gmail.com"
    assert body["verified"] is False
    assert body["primary"] is False
    assert isinstance(body["created_at"], str)


def test_create_duplicate(verified_user_with_token: tuple[Account, str], db_session: Session):
    assert db_session.query(Email).count() == 1

    user, auth_token = verified_user_with_token
    response = client.post(
        "/accounts/emails",
        json={"address": user.emails[0].address},
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert db_session.query(Email).count() == 1


def test_set_primary(verified_user_with_token: tuple[Account, str], db_session: Session):
    user, auth_token = verified_user_with_token
    email_crud = EmailCRUD(db_session, user)
    email = email_crud.create("gopaul0510@gmail.com")
    email_crud.commit(email)
    assert email.primary is False
    response = client.patch(f"/accounts/emails/{email.id}/primary", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT
    emails = db_session.query(Email).filter_by(account_id=user.id)
    assert emails.count() == 2
    primary_email_query = emails.filter_by(primary=True)
    assert primary_email_query.count() == 1
    assert primary_email_query.one().address == "gopaul0510@gmail.com"


def test_set_primary_invalid_email(verified_user_with_token: tuple[Account, str], db_session: Session):
    auth_token = verified_user_with_token[1]
    response = client.patch(f"/accounts/emails/ffffffff-ffff-ffff-ffff-ffffffffffff/primary", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
