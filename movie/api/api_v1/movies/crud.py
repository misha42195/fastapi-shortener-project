import logging

from pydantic import BaseModel
from redis import Redis

from core import config
from schemas.muvies import (
    CreateMovies,
    Movies,
    MoviesPartialUpdate,
    UpdateMovies,
)

log = logging.getLogger(__name__)

redis_movies = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_MOVIES_DB_NUM,
    decode_responses=True,
)


class MoviesBaseErr(Exception):
    """
    Base exception class for movie-related errors.
    """


class MovieAlreadyExistsError(MoviesBaseErr):
    """
    Raised when attempting to create a movie that already exists.
    """


class MoviesStorage(BaseModel):
    movies_slug: dict[str, Movies] = {}

    def save_movie_in_db(
        self,
        movie: Movies,
    ) -> None:
        redis_movies.hset(
            name=config.REDIS_MOVIES_SET_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )

    def get_movies(self) -> list[Movies]:
        log.info("Получение списка фильмов.")
        movies_list = redis_movies.hvals(
            config.REDIS_MOVIES_SET_NAME,
        )
        movies = [Movies.model_validate_json(movies) for movies in movies_list]
        log.info("Список фильмов %s", movies)

        return movies

    def exists(
        self,
        slug: str,
    ) -> bool:
        return bool(
            redis_movies.hexists(
                config.REDIS_MOVIES_SET_NAME,
                slug,
            )
        )

    def get_by_slug(self, slug: str) -> Movies | None:
        log.info("получение фильма: %s", slug)
        movie_json = redis_movies.hget(
            name=config.REDIS_MOVIES_SET_NAME,
            key=slug,
        )
        if movie_json:
            return Movies.model_validate_json(movie_json)
        return None

    def create_movie(
        self,
        movie_in: CreateMovies,
    ) -> Movies:
        movie = Movies(
            **movie_in.model_dump(),
        )
        self.save_movie_in_db(movie)

        log.info("Создание нового фильма = %s", movie.slug)
        return movie

    def create_raise_already_exists(
        self,
        movie_in: CreateMovies,
    ) -> Movies:
        if not self.exists(movie_in.slug):
            return movie_storage.create_movie(movie_in)
        raise MovieAlreadyExistsError(movie_in.slug)

    def delete_by_slug(
        self,
        slug: str,
    ) -> None:
        redis_movies.hdel(
            config.REDIS_MOVIES_SET_NAME,
            slug,
        )
        log.info("Удаление фильма")

    def delete(self, movie: Movies | CreateMovies) -> None:
        self.delete_by_slug(slug=movie.slug)
        log.info("Удаление фильма")

    def update_movie(
        self,
        movie: Movies,
        movie_data_in: UpdateMovies,
    ) -> Movies:
        for k, v in movie_data_in:
            setattr(movie, k, v)
        self.save_movie_in_db(movie)
        log.info("Фильм обновлен с %s до %s", movie.director, movie_data_in.description)
        return movie

    def movie_partial_update(
        self,
        movies: Movies,
        movies_in: MoviesPartialUpdate,
    ) -> Movies:
        for field_mane, value in movies_in.model_dump(exclude_unset=True).items():
            setattr(movies, field_mane, value)
        self.save_movie_in_db(movies)
        return movies


movie_storage = MoviesStorage()
