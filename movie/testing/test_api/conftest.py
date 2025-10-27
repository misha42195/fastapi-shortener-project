from collections.abc import Generator

import pytest
from api.api_v1.auth.services import redis_tokens
from starlette.testclient import TestClient

from main import app


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
