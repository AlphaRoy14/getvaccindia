from typing import Generator
from time import sleep
from unittest import mock

import os
import pytest
import docker
from fastapi.testclient import TestClient
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from core.config import settings
from core.utils import fm
from main import app


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app=app) as c:
        yield c


@pytest.fixture(scope="session")
def get_fm() -> FastMail:
    yield fm


@pytest.fixture(scope="session", autouse=True)
def mongo_docker() -> None:
    client = docker.from_env()
    mongo_container = client.containers.run(
        image="mongo", ports={"27017": "27017"}, detach=True, remove=True
    )
    # make sure the container is running 🤞🏻
    while mongo_container.status != "running":
        sleep(2)
        mongo_container.reload()

    yield

    mongo_container.stop()


@pytest.fixture(autouse=True, scope="session")
def mock_settings_env_var():
    with mock.patch.dict(os.environ, {"MONGODB_URL": "mongodb://127.0.0.1:27017/"}):
        yield
