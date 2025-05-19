import logging

from pydantic import BaseModel, ValidationError

from core.config import PATH_TO_MOVIE_FILE

from schemas.muvies import (
    Movies,
    CreateMovies,
    UpdateMovies,
    MoviesPartialUpdate,
)

log = logging.getLogger(__name__)


class MoviesStorage(BaseModel):
    movies_slug: dict[str, Movies] = {}

    def save_movie(self) -> None:
        for _ in range(30_000):
            PATH_TO_MOVIE_FILE.write_text(movie_storage.model_dump_json(indent=2))
        PATH_TO_MOVIE_FILE.write_text(movie_storage.model_dump_json(indent=2))
        log.info("Фильм сохранен в файл.")

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
        return list(self.movies_slug.values())

    def get_by_slug(self, slug) -> Movies:
        log.info("получение фильма: %s", self.movies_slug.get(slug))
        return self.movies_slug.get(slug)

    def create_movie(self, movie_in: CreateMovies) -> Movies:
        movie = Movies(
            **movie_in.model_dump(),
        )
        self.movies_slug[movie.slug] = movie
        log.info("Создание нового фильма = %s", movie.slug)
        return movie

    def delete_by_slug(self, slug) -> None:
        self.movies_slug.pop(slug)
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
        log.info("Фильм обновлен с %s до %s", movie.director, movie_data_in.description)
        return movie

    def movie_partial_update(
        self,
        movies: Movies,
        movies_in: MoviesPartialUpdate,
    ) -> Movies:
        for field_mane, value in movies_in.model_dump(exclude_unset=True).items():
            setattr(movies, field_mane, value)
        return movies


# movie_storage = MoviesStorage()
#
# movie_storage.create_movie(
#     CreateMovies(
#         slug="shoushenka",
#         title="Побег из Шоушенка",
#         description="Два заключённых сближаются за годы заключения, находя утешение и надежду на свободу.",
#         release_year=date(1994, 9, 22),
#         director="Фрэнк Дарабонт",
#     )
# )
# movie_storage.create_movie(
#     CreateMovies(
#         slug="father",
#         title="Крёстный отец",
#         description="Стареющий глава мафиозной семьи передаёт власть своему неохотному сыну.",
#         release_year=date(1972, 3, 24),
#         director="Фрэнсис Форд Коппола",
#     )
# )
# movie_storage.create_movie(
#     CreateMovies(
#         slug="start",
#         title="Начало",
#         description="Вор использует технологию проникновения в сны, чтобы внедрить идею в сознание цели.",
#         release_year=date(2010, 7, 16),
#         director="Кристофер Нолан",
#     ),
# )

movie_storage = MoviesStorage()
