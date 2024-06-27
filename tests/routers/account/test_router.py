from re import match
from fastapi import status
from sqlalchemy.orm import Session
from app.models import Account
from ... import client

datetime_format = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}$'


def test_register(db_session: Session):
    assert db_session.query(Account).count() == 0

    response = client.post("/accounts/register", json={
        "name": "Girish Gopaul",
        "email": "girish@gopaul.me",
        "password": "JustAPass01!"
    })
    body = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(body["id"], str)
    assert body["name"] == "Girish Gopaul"
    assert match(datetime_format, body["created_at"])
    assert db_session.query(Account).count() == 1


def test_register_duplicate(verified_user: Account, db_session: Session):
    assert db_session.query(Account).count() == 1

    response = client.post("/accounts/register", json={
        "name": "Girish Gopaul",
        "email": verified_user.emails[0].address,
        "password": "JustAPass01!"
    })

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert db_session.query(Account).count() == 1


def test_me(verified_user_with_token: tuple[Account, str]):
    _, auth_token = verified_user_with_token
    response = client.get("/accounts/me", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    body = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.headers.get('X-Token'), str)
    assert body["name"] == "Girish Gopaul"
    assert match(datetime_format, body["created_at"])


def test_me_with_invalid_token(verified_user_with_token: tuple[Account, str]):
    auth_token = verified_user_with_token[1]
    response = client.get("/accounts/me", headers={
        "Authorization": f"Bearer {auth_token}a"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login(verified_user: Account):
    response = client.post("/accounts/login", json={
        "email": verified_user.emails[0].address,
        "password": "JustAPass01!"
    })
    body = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.headers.get('X-Token'), str)
    assert body["name"] == "Girish Gopaul"
    assert match(datetime_format, body["created_at"])


def test_login_with_invalid_password(verified_user: Account):
    response = client.post("/accounts/login", json={
        "email": verified_user.emails[0].address,
        "password": "FakePass01!"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
