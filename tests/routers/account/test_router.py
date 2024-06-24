from re import match
from fastapi import status
from ... import client


def test_register():
    response = client.post("/accounts/register", json={
        "name": "Girish Gopaul",
        "email": "girish@gopaul.me",
        "password": "JustAPass01!"
    })
    body = response.json()
    datetime_format = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}$'

    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(body["id"], str)
    assert body["name"] == "Girish Gopaul"
    assert body["email"] == "girish@gopaul.me"
    assert not body["email_verified"]
    assert match(datetime_format, body["created_at"])
