from datetime import date
from unittest import TestCase
from movie.schemas.muvies import (
    CreateMovies,
    Movies,
    UpdateMovies,
    MoviesPartialUpdate,
)


class MoviesPartialUpdateTestCase(TestCase):
    def create_movie(self) -> MoviesPartialUpdate:
        create_movie = MoviesPartialUpdate(
            title="test_partial_title",
            description="test_partial_description",
            release_year=date(2025, 6, 10),
            director="test_patrial_director",
        )
        return create_movie

    def test_partial_update_movie_for_scheme(self) -> None:
        partial_movie = self.create_movie()
        movie = Movies(
            slug="test_partial_update",
            **partial_movie.model_dump(exclude_unset=True),
        )
        self.assertEqual(partial_movie.title, movie.title)
        self.assertEqual(partial_movie.description, movie.description)
        self.assertEqual(partial_movie.release_year, movie.release_year)
        self.assertEqual(partial_movie.director, movie.director)


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
            # "",  # невалидно (пустая строка)
            # "A" * 300,  # невалидно (слишком длинное название)
        ]
        for title in title_list:
            with self.subTest(
                title=title, msg=f"title {title}"
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
            # None,  # зависит от схемы (может быть валидным)
        ]
        for description in description_list:
            with self.subTest(
                description=description, msg=f"title {description}"
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
            # "2025-06-10",  # невалидно, если не преобразуется
            # "not-a-date",  # невалидно
            # None,  # невалидно
            # 20250610,  # невалидно
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
            "test-slug",  # валидно
            # "slug_with_underscores",  # валидно
            # "invalid slug",  # невалидно (пробелы)
            # "slug$",  # невалидно (спецсимволы)
            # "",  # невалидно
            # None,  # невалидно
            # 123,  # невалидно
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
            "Christopher Nolan",  # валидно
            # "",  # невалидно (пусто)
            "A",  # валидно, если нет ограничений
            # None,  # невалидно
            # 999,  # невалидно
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
