from datetime import date
from unittest import TestCase
from movie.schemas.muvies import (
    CreateMovies,
    Movies,
    UpdateMovies,
)


class UpdateMoviesTestCase(TestCase):
    def test_update_movie_for_scheme(self) -> None:
        update_movie = UpdateMovies(
            title="test_update_title",
            description="test_update_description",
            release_year=date(2025, 6, 10),
            director="test_update_director",
        )
        movie = Movies(
            slug="test_exclude_slug",
            **update_movie.model_dump(exclude_unset=True),
        )
        self.assertEqual(update_movie.title, movie.title)
        self.assertEqual(update_movie.description, movie.description)
        self.assertEqual(update_movie.release_year, movie.release_year)
        self.assertEqual(update_movie.director, movie.director)


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
        self.assertEqual(movie_in.title, movie.title)
        self.assertEqual(movie_in.description, movie.description)
        self.assertEqual(movie_in.release_year, movie.release_year)
        self.assertEqual(movie_in.slug, movie.slug)
        self.assertEqual(movie_in.director, movie.director)
