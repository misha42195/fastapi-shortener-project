import random
import string
from collections.abc import Generator
from datetime import date
from os import getenv

import pytest
from _pytest.fixtures import SubRequest

from api.api_v1.movies import movie_storage
from schemas.muvies import CreateMovies, Movies


@pytest.fixture(
    scope="session",
    autouse=True,
)
def check_testing_env() -> None:
    if getenv("TESTING") != "1":
        pytest.exit("The environment is not ready for tests")


def build_movie_create(
    slug: str,
    title: str = "test title",
    description: str = "test description",
) -> CreateMovies:
    movie_create = CreateMovies(
        title=title,
        description=description,
        release_year=date(2025, 10, 1),
        director="test director",
        slug=slug,
    )
    return movie_create


def build_movie_create_random_slug(
    description: str = "test description",
    title: str = "test title",
) -> CreateMovies:
    slug = "".join(random.choices(string.ascii_lowercase, k=8))
    movie_create = build_movie_create(
        slug,
        description=description,
        title=title,
    )
    return movie_create


def create_movie(
    slug: str,
    description: str,
    title: str,
) -> Movies:
    movie_in = build_movie_create(
        slug=slug,
        description=description,
        title=title,
    )
    movie_create = movie_storage.create_movie(movie_in)
    return movie_create


def create_movie_random_slug(
    description: str = "test description",
    title: str = "test title",
) -> Movies:
    movie_in = build_movie_create_random_slug(
        description=description,
        title=title,
    )
    movie_create = movie_storage.create_movie(movie_in)
    return movie_create


@pytest.fixture(
    scope="module",
    params=[
        pytest.param("slug", id="normal slug"),  # обычный слаг
        pytest.param("sl", id="short slug"),  # короткий слаг
        pytest.param("abs", id="min slug"),  # минимально допустимый
        pytest.param("max-som-ts", id="max slug"),  # максимально допустимый
    ],
)
def movie(request: SubRequest) -> Generator[CreateMovies]:
    movie_create = build_movie_create(slug=request.param)
    yield movie_create
    movie_storage.delete(movie_create)
