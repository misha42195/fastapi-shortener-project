import random
import string
from copy import deepcopy
from datetime import date
from typing import Any, Generator
from unittest import TestCase

import pytest
from pydantic import ValidationError

from schemas.muvies import (
    CreateMovies,
    Movies,
    MoviesPartialUpdate,
    UpdateMovies,
)
from storage.movies.crud import movie_storage
from storage.movies.exeptions import MovieAlreadyExistsError


@pytest.fixture()
def movie() -> Generator[Any, Any, None]:
    movie_in = CreateMovies(
        title="test title",
        description="test description",
        release_year=date(2025, 5, 23),
        director="test director",
        slug="".join(random.choices(string.ascii_lowercase, k=8)),
    )
    movie = movie_storage.create_movie(movie_in)
    yield movie
    movie_storage.delete(movie)


class MoviesPartialUpdateTestCase(TestCase):
    def original_movie(self) -> Movies:
        create_movie = Movies(
            title="test_partial_title",
            description="test_partial_description",
            release_year=date(2025, 6, 10),
            director="test_patrial_director",
            slug="test_slug",
        )
        return create_movie

    def test_partial_update_movie_for_scheme(self) -> None:
        original_movie = self.original_movie()
        original_data = deepcopy(original_movie.__dict__.copy())

        empty_movie = MoviesPartialUpdate()
        for key, val in empty_movie.model_dump(exclude_unset=True).items():
            setattr(original_movie, key, val)
        self.assertEqual(original_movie.__dict__, original_data)


class UpdateMoviesTestCase(TestCase):
    def test_update_movie_for_scheme(self) -> None:
        update_movie = UpdateMovies(
            title="test_update_title",
            description="test_update_description",
            release_year=date(2025, 6, 10),
            director="test_update_director",
        )
        movie = Movies(
            slug="test_slug",
            **update_movie.model_dump(),
        )
        self.assertEqual(update_movie.title, movie.title)
        self.assertEqual(update_movie.description, movie.description)
        self.assertEqual(update_movie.release_year, movie.release_year)
        self.assertEqual(update_movie.director, movie.director)


class CreateMoviesTestCase(TestCase):
    @classmethod
    def create_validation_movie(cls) -> CreateMovies:
        movie = CreateMovies(
            title="test title",
            description="test descript",
            release_year=date(2025, 6, 10),
            slug="test-slug",
            director="test director",
        )
        return movie

    def test_slug_to_short(self) -> None:
        with self.assertRaises(ValidationError) as exc_info:
            CreateMovies(
                title="test title",
                description="test descript",
                release_year=date(2025, 6, 10),
                slug="d",
                director="test director",
            )
        result = exc_info.exception.errors()[0]["type"]
        expected_result = "string_too_short"
        print(f"{result} == {expected_result}")
        self.assertEqual(expected_result, result)

    def test_slug_to_short_with_regex(self) -> None:
        with self.assertRaisesRegex(
            ValidationError,
            expected_regex="String should have at least 3 characters",
        ):
            CreateMovies(
                title="test title",
                description="test descript",
                release_year=date(2025, 6, 10),
                slug="d",
                director="test director",
            )

    def test_create_movie_for_scheme(self) -> None:
        """проверка полей slug и description"""
        movie_in = CreateMovies(
            title="test title",
            description="test descript",
            release_year=date(2025, 6, 10),
            slug="test-slug",
            director="test director",
        )
        movie = Movies(
            **movie_in.model_dump(),
        )
        self.assertEqual(movie_in.title, movie.title)
        self.assertEqual(movie_in.description, movie.description)
        self.assertEqual(movie_in.release_year, movie.release_year)
        self.assertEqual(movie_in.slug, movie.slug)
        self.assertEqual(movie_in.director, movie.director)


class CreateAFilmWithVariousAttributesTestCase(TestCase):

    def test_create_movie_accepts_different_values(self) -> None:
        title_list = [
            "Inception",  # валидно
            # "", # невалидно (пустая строка)
            # "A" * 300, # невалидно (слишком длинное название)
        ]
        for title in title_list:
            with self.subTest(
                title=title,
                msg=f"title {title}",
            ):  # msg=f"title {description}"
                movie_in = CreateMovies(
                    title=title,
                    description="good film about life",
                    release_year=date(2025, 5, 23),
                    slug="test_slug",
                    director="test_director",
                )
                movie = Movies(**movie_in.model_dump())
                self.assertEqual(title, movie.title)

        description_list = [
            "An epic movie.",  # валидно
            "to_string",  # возможно валидно, если пустое допустимо
            "Фильм о будущем.",  # валидно (юникод)
            "12344",  # невалидно (не строка)
            # None, # зависит от схемы (может быть валидным)
        ]
        for description in description_list:
            with self.subTest(
                description=description,
                msg=f"title {description}",
            ):  #  msg=f"title {description}"
                movie_in = CreateMovies(
                    title="test_title",
                    description=description,
                    release_year=date(2025, 5, 23),
                    slug="test_slug",
                    director="test_director",
                )
                movie = Movies(**movie_in.model_dump())
                self.assertEqual(description, movie.description)
        release_year_list = [
            date(2025, 6, 10),  # валидно
            date(1994, 10, 14),  # валидно
        ]
        for release_year in release_year_list:
            with self.subTest(release_year=release_year, msg=f"title {release_year}"):
                movie_in = CreateMovies(
                    title="test_title",
                    description="test description for this movie",
                    release_year=release_year,
                    slug="test_slug",
                    director="test_director",
                )
                movie = Movies(**movie_in.model_dump())
                self.assertEqual(release_year, movie.release_year)

        slug_list = [
            "test-slug",
            "slug$",
        ]
        for slug in slug_list:
            with self.subTest(slug=slug, msg=f"slug {slug}"):  # msg=f"title {slug}"
                movie_in = CreateMovies(
                    title="test_title",
                    description="test description for this movie",
                    release_year=date(2025, 5, 23),
                    slug=slug,
                    director="test_director",
                )
                movie = Movies(**movie_in.model_dump())
                self.assertEqual(slug, movie.slug)

        director_list = [
            "Christopher Nolan",
            "A",
        ]
        for director in director_list:
            with self.subTest(director=director, msg=f"title {director}"):
                movie_in = CreateMovies(
                    title="test_title",
                    description="test description for this movie",
                    release_year=date(2025, 5, 23),
                    slug="test_slug",
                    director=director,
                )
                movie = Movies(**movie_in.model_dump())
                self.assertEqual(director, movie.director)


def test_create_or_raise_already_exists(movie: Movies) -> None:
    create_movie = CreateMovies(**movie.model_dump())
    with pytest.raises(MovieAlreadyExistsError, match=movie.slug) as ext:
        movie_storage.create_raise_already_exists(create_movie)
    assert ext.value.args[0] == movie.slug
