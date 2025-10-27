from collections.abc import Generator

import pytest
from starlette.testclient import TestClient

from main import app
from services.auth import redis_tokens


@pytest.fixture()
def client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def auth_token() -> Generator[str]:
    token = redis_tokens.add_token()
    yield token
    redis_tokens.delete_token(token)


@pytest.fixture(scope="module")
def auth_client(auth_token: str) -> Generator[TestClient, None, None]:
    headers = {"Authorization": f"Bearer {auth_token}"}
    with TestClient(app) as client:
        client.headers.update(headers=headers)
        yield client
