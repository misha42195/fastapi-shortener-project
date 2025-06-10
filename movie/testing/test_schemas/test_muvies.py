from datetime import date
from unittest import TestCase
from schemas.muvies import (
    CreateMovies,
    Movies,
)


class CreateMoviesTestCase(TestCase):

    def test_create_movie_for_scheme(self) -> None:
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
        self.assertEqual(
            movie_in.title,
            movie.title,
        )
        self.assertEqual(
            movie_in.description,
            movie.description,
        )
        self.assertEqual(
            movie_in.release_year,
            movie.release_year,
        )
        self.assertEqual(
            movie_in.slug,
            movie.slug,
        )
        self.assertEqual(
            movie_in.director,
            movie.director,
        )
