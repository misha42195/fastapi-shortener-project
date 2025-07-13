import random
import string
from collections.abc import Generator
from datetime import date

import pytest
from _pytest.fixtures import SubRequest
from starlette.testclient import TestClient

from api.api_v1.auth.services import redis_tokens
from api.api_v1.movies import movie_storage
from main import app
from schemas.muvies import Movie, CreateMovies


@pytest.fixture()
def client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def auth_token() -> Generator[str]:
    token = redis_tokens.generate_and_save_token()
    yield token
    redis_tokens.delete_token(token)


@pytest.fixture(scope="module")
def auth_client(auth_token) -> Generator[TestClient]:
    headers = {"Authorization": f"Bearer {auth_token}"}
    with TestClient(app) as client:
        client.headers.update(headers=headers)
        yield client


@pytest.fixture(
    scope="module",
    params=[
        pytest.param("slug", id="normal slug"),  # обычный слаг
        pytest.param("sl", id="short slug"),  # короткий слаг
        pytest.param("abs", id="min slug"),  # минимально допустимый
        pytest.param("max-som-ts", id="max slug"),  # максимально допустимый
    ],
)
def movie(request: SubRequest) -> Generator[Movie]:
    print(request.param)
    movie_in = CreateMovies(
        title="Test title",
        description="Test description",
        release_year=date(2025, 10, 10),
        director="Test director",
        slug=request.param,
    )

    movie = movie_storage.create_movie(movie_in=movie_in)
    yield movie
    movie_storage.delete(movie)
