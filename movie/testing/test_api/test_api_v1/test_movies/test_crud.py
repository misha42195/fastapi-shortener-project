import random
import string
from datetime import date
from typing import ClassVar
from unittest import TestCase

import pytest

from api.api_v1.movies import movie_storage
from schemas.muvies import (
    CreateMovies,
    Movies,
    MoviesPartialUpdate,
    UpdateMovies,
)


def total(a: int, b: int) -> int:
    return a + b


@pytest.fixture(scope="module")
def movie() -> Movies:
    mov = CreateMovies(
        title="test title movie",
        description="A test movie description",
        release_year=date(2024, 2, 10),
        director="test director",
        slug="".join(random.choices(string.ascii_lowercase, k=8)),
    )
    return movie_storage.create_movie(mov)


class MovieStorageGetTestCase(TestCase):
    MOVIES_COUNT = 3
    movies_list_in_cls: ClassVar[list[Movies]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.movies_list_in_cls = [movie() for _ in range(cls.MOVIES_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for movie in cls.movies_list_in_cls:
            movie_storage.delete(movie)

    def test_get_movie_list(self) -> None:
        movies_in_base = movie_storage.get_movies()
        movies_in_base_slug = {mv.slug for mv in movies_in_base}
        movies_in_cls_slug = {mv.slug for mv in self.movies_list_in_cls}
        self.assertEqual(movies_in_base_slug, movies_in_cls_slug)

    def test_get_movie_by_slug(self) -> None:
        for movie in self.movies_list_in_cls:
            # 1. Проверка на None должна быть ДО обращения к атрибутам
            assert (
                movie is not None
            ), "Movie object in movies_list_in_cls cannot be None"

            with self.subTest(movie=movie, msg=f"Validate can by slug {movie.slug!r}"):
                # 2. Получаем фильм по slug
                movie_in_base_slug = movie_storage.get_by_slug(movie.slug)

                # 3. Проверяем, что фильм найден в хранилище
                assert (
                    movie_in_base_slug is not None
                ), f"Movie with slug {movie.slug!r} not found in storage"

                # 4. Теперь оба объекта гарантированно не None
                self.assertEqual(movie.slug, movie_in_base_slug.slug)


class MovieStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.test_movie = movie()

    def test_update_movie(self) -> None:
        movie_update = UpdateMovies(**self.test_movie.model_dump())
        source_movie = movie_update.title
        movie_update.title += "a new string"

        updated_movie = movie_storage.update_movie(
            movie=self.test_movie,
            movie_data_in=movie_update,
        )
        self.assertNotEqual(source_movie, updated_movie.title)
        self.assertEqual(movie_update, UpdateMovies(**updated_movie.model_dump()))

    def test_update_partial_movie(self) -> None:
        partial_movie_update = MoviesPartialUpdate(
            description=self.test_movie.description + "(descript)"
        )
        source_description = self.test_movie.description
        updated_movie_partial = movie_storage.movie_partial_update(
            self.test_movie,
            partial_movie_update,
        )
        self.assertNotEqual(source_description, updated_movie_partial.description)
        self.assertEqual(
            partial_movie_update.description, updated_movie_partial.description
        )

    def tearDown(self) -> None:
        movie_storage.delete(self.test_movie)

    def test_total(self) -> None:
        num_a = random.randrange(1, 100)
        num_b = random.randrange(1, 100)

        result = total(num_a, num_b)
        expected_result = num_a + num_b

        print(expected_result)
        self.assertEqual(result, expected_result)
