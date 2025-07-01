import random
import string
from datetime import date

from typing import ClassVar
from unittest import TestCase


from api.api_v1.movies import movie_storage
from schemas.muvies import (
    CreateMovies,
    Movie,
    UpdateMovies,
    MoviesPartialUpdate,
)


def total(a: int, b: int) -> int:
    return a + b


def create_movie() -> Movie:
    movie = CreateMovies(
        title="test title movie",
        description="A test movie description",
        release_year=date(2024, 2, 10),
        director="test director",
        slug="".join(random.choices(string.ascii_lowercase, k=8)),
    )
    return movie_storage.create_movie(movie)


class MovieStorageGetTestCase(TestCase):
    MOVIES_COUNT = 3
    movies_list_in_cls: ClassVar[list[Movie]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.movies_list_in_cls = [create_movie() for _ in range(cls.MOVIES_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for movie in cls.movies_list_in_cls:
            movie_storage.delete(movie)

    def test_get_movie_list(self) -> None:
        movies_in_base = movie_storage.get_movies()  # фильмы из базы
        movies_in_base_slug = {mv.slug for mv in movies_in_base}
        movies_in_cls_slug = {mv.slug for mv in self.movies_list_in_cls}
        self.assertEqual(movies_in_base_slug, movies_in_cls_slug)

    def test_get_movie_by_slug(self) -> None:
        for movie in self.movies_list_in_cls:
            with self.subTest(movie=movie, msg=f"Validate can by slug {movie.slug!r}"):
                movie_in_base_slug = movie_storage.get_by_slug(movie.slug)
                self.assertEqual(movie.slug, movie_in_base_slug.slug)


class MovieStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.test_movie = create_movie()

    def test_update_movie(self) -> None:
        """ """
        movie_update = UpdateMovies(
            **self.test_movie.model_dump()
        )  # фильм для обновления, начальное состояние
        source_movie = movie_update.title  # фиксируем начальное состояние поля title
        movie_update.title += "a new string"  # вносим изменения в фильм, далее его поля используем для изменения

        updated_movie = movie_storage.update_movie(  # обновляем фильм используя значения измененного фильма
            movie=self.test_movie,
            movie_data_in=movie_update,
        )
        self.assertNotEqual(
            source_movie, updated_movie.title
        )  # сравним старое значение поля title и измененного
        self.assertEqual(
            movie_update, UpdateMovies(**updated_movie.model_dump())
        )  # одинаковые ли объекты фильмы
        # обновленный фильм и поля которые

    def test_update_partial_movie(self) -> None:
        """тест на частичное обновление данных"""
        partial_movie_update = MoviesPartialUpdate(
            description=self.test_movie.description + "(descript)"
        )
        source_description = self.test_movie.description  # фиксируем значение
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
