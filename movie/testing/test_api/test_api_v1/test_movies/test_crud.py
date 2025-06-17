import random
import string
from datetime import date
from importlib.util import source_hash
from os import getenv
from unittest import TestCase

from api.api_v1.movies import movie_storage
from schemas.muvies import (
    CreateMovies,
    Movies,
    UpdateMovies,
    MoviesPartialUpdate,
)

if getenv("TESTING") != "1":
    raise OSError(
        "To start the test, check the values of the variable environment (REDIS_PORT, TESTING)"
    )


def total(a: int, b: int) -> int:
    return a + b


class MovieStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.test_movie = self.create_movie()

    def create_movie(self) -> Movies:
        movie = CreateMovies(
            title="test title movie",
            description="A test movie description",
            release_year=date(2024, 2, 10),
            director="test director",
            slug="".join(random.choices(string.ascii_lowercase, k=8)),
        )
        return movie_storage.create_movie(movie)

    def test_update_movie(self) -> None:
        """
        1) создадим фильм на основе созданного фильма, который будем обновлять
        2) зафиксируем поле title, далее изменим это поле
        3) создадим фильм из класса UpdatedMovie(изменили его поле title)
        4) сравним поля зафиксированного фильма с полем фильма, который поменяли
        5) сравним фильм, со значениями который хотели изменить с измененными полями полученного фильма
        то есть проверим значения которые хотели установить с полученным фильмом
        """
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
