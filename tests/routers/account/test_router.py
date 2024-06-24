from re import match
from fastapi import status
from app.models import Account
from app.utils import encode_auth_token
from ... import client

datetime_format = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}$'


def test_register():
    response = client.post("/accounts/register", json={
        "name": "Girish Gopaul",
        "email": "girish@gopaul.me",
        "password": "JustAPass01!"
    })
    body = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(body["id"], str)
    assert body["name"] == "Girish Gopaul"
    assert body["email"] == "girish@gopaul.me"
    assert not body["email_verified"]
    assert match(datetime_format, body["created_at"])


def test_me(created_user: Account):
    auth_token = encode_auth_token(created_user.id)
    response = client.get("/accounts/me", headers={"Authorization": f"Bearer {auth_token}"})
    body = response.json()
    assert response.status_code == 200
    assert isinstance(response.headers.get('X-Token'), str)
    assert body["name"] == "Girish Gopaul"
    assert body["email"] == "girish@gopaul.me"
    assert body["email_verified"]
    assert match(datetime_format, body["created_at"])
