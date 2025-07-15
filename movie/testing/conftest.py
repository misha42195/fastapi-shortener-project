import random
import string
from collections.abc import Generator
from datetime import date
from os import getenv
from typing import Generator

import pytest
from _pytest.fixtures import SubRequest

from api.api_v1.movies import movie_storage
from schemas.muvies import Movie, CreateMovies

if getenv("TESTING") != "1":
    pytest.exit("The environment is not ready for tests")


def build_movie_create(slug: str) -> CreateMovies:
    movie_create = CreateMovies(
        title="test title",
        description="test description",
        release_year=date(2025, 10, 1),
        director="test director",
        slug=slug,
    )
    return movie_create


def build_movie_create_random_slug() -> CreateMovies:
    slug = "".join(random.choices(string.ascii_lowercase, k=8))
    movie_create = build_movie_create(slug)
    return movie_create


def create_movie(slug: str) -> Movie:
    movie_in = build_movie_create(slug=slug)
    movie_create = movie_storage.create_movie(movie_in)
    return movie_create


def create_movie_random_slug() -> Movie:
    movie_in = build_movie_create_random_slug()
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
def movie(request: SubRequest) -> Generator[CreateMovies, None, None]:
    movie_create = build_movie_create(slug=request.param)
    yield movie_create
    movie_storage.delete(movie_create)
