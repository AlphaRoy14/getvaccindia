import pytest
from core.config import settings
from fastapi.testclient import TestClient
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import crud


def test_subscriber_create(client: TestClient, get_fm: FastMail):
    """
    test adding a subscriber
    """
    get_fm.config.SUPPRESS_SEND = 1
    payload = {
        "name": "test",
        "email": "test@example.com",
        "zip_code": 123452,
        "vaccine_doze": [2],
        "state": "Delhi",
    }
    with get_fm.record_messages() as outbox:
        r = client.post(url=f"{settings.API_V1_STR}/user/subscribe", json=payload)
        user = r.json()
        assert user
        assert r.status_code == 201
        assert outbox[0]["To"] == "test@example.com"


def test_incorrect_semantic_subscriber_create(client: TestClient, get_fm: FastMail):
    """
    test incorrect json payload structure
    """

    payload = {
        "name": "test",
        "email": "test@example.com",
        "zip_code": 123452,
        "vaccine_doze": 2,  # ~ shold be a list
        "state": "Delhi",
    }

    with get_fm.record_messages() as outbox:
        r = client.post(url=f"{settings.API_V1_STR}/user/subscribe", json=payload)
        assert r.status_code == 422
