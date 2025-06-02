import logging

from pydantic import BaseModel, ValidationError
from redis import Redis

from core import config
from core.config import PATH_TO_MOVIE_FILE

from schemas.muvies import (
    Movies,
    CreateMovies,
    UpdateMovies,
    MoviesPartialUpdate,
)

log = logging.getLogger(__name__)

redis_movies = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_MOVIES_DB_NUM,
    decode_responses=True,
)


class MoviesStorage(BaseModel):
    movies_slug: dict[str, Movies] = {}

    def save_movie(self) -> None:
        for _ in range(30_000):
            PATH_TO_MOVIE_FILE.write_text(movie_storage.model_dump_json(indent=2))
        PATH_TO_MOVIE_FILE.write_text(movie_storage.model_dump_json(indent=2))
        log.info("Фильм сохранен в файл.")

    def save_movie_in_db(
        self,
        movie: Movies,
    ):
        redis_movies.hset(
            name=config.REDIS_MOVIES_SET_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )

    def load_movie(self) -> "MoviesStorage":
        if not PATH_TO_MOVIE_FILE.exists():
            log.info("Файл хранения фильмов не существует")
            return MoviesStorage()

        return self.__class__.model_validate_json(PATH_TO_MOVIE_FILE.read_text())

    def init_storage_from_state(self) -> None:
        try:
            data = MoviesStorage().load_movie()
        except ValidationError:
            self.save_movie()
            log.warning("Восстановленные данные из файла хранения.")
            return

        self.movies_slug.update(
            data.movies_slug,
        )
        log.warning("Восстановленные данные из файла хранения.")

    def get_movies(self) -> list[Movies]:
        log.info("Получение списка фильмов.")
        movies_list = redis_movies.hvals(
            config.REDIS_MOVIES_SET_NAME,
        )
        movies = [Movies.model_validate_json(movies) for movies in movies_list]
        log.info("Список фильмов %s", movies)

        return movies

    def get_by_slug(self, slug) -> Movies | None:
        log.info("получение фильма: %s", self.movies_slug.get(slug))

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

    def delete_by_slug(
        self,
        slug: str,
    ) -> None:
        redis_movies.hdel(
            config.REDIS_MOVIES_SET_NAME,
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


movie_storage = MoviesStorage()
