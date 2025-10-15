__all__ = ("MoviesStorage",)
import logging

from pydantic import BaseModel
from redis import Redis

from core.config import settings
from schemas.muvies import (
    CreateMovies,
    Movies,
    MoviesPartialUpdate,
    UpdateMovies,
)
from storage.movies.exeptions import MovieAlreadyExistsError

log = logging.getLogger(__name__)

redis_movies = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.movies,
    decode_responses=True,
)


class MoviesStorage(BaseModel):
    hash_name: str

    def save_movie_in_db(
        self,
        movie: Movies,
    ) -> None:
        redis_movies.hset(
            name=self.hash_name,
            key=movie.slug,
            value=movie.model_dump_json(),
        )

    def get_movies(self) -> list[Movies]:
        log.info("Получение списка фильмов.")
        movies_list = redis_movies.hvals(
            self.hash_name,
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
                self.hash_name,
                slug,
            ),
        )

    def get_by_slug(self, slug: str) -> Movies | None:
        log.info("получение фильма: %s", slug)
        movie_json = redis_movies.hget(
            name=self.hash_name,
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
            return movi_storage.create_movie(movie_in)
        raise MovieAlreadyExistsError(movie_in.slug)

    def delete_by_slug(
        self,
        slug: str,
    ) -> None:
        redis_movies.hdel(
            self.hash_name,
            slug,
        )
        log.info("Удаление фильма")

    def delete(self, movie: Movies) -> None:
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


movi_storage = MoviesStorage(
    hash_name=settings.redis.collections_names.movies_hash_name,
)
