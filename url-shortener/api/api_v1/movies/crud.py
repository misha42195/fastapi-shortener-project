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
        PATH_TO_MOVIE_FILE.write_text(movie_storage.model_dump_json(indent=2))
        log.info("Saved movie to storage file.")

    def load_movie(self) -> "MoviesStorage":
        if not PATH_TO_MOVIE_FILE.exists():
            log.info("Movie storage file doesn't exist")
            return MoviesStorage()

        return self.__class__.model_validate_json(PATH_TO_MOVIE_FILE.read_text())

    def init_storage_from_state(self) -> None:
        try:
            data = MoviesStorage().load_movie()
        except ValidationError:
            self.save_movie()
            log.warning("Recovered data from storage file.")
            return

        self.movies_slug.update(
            data.movies_slug,
        )
        log.warning("Recovered data from storage file.")

    def get_movies(self) -> list[Movies]:
        log.info("Возврат списка фильмов.")
        return list(self.movies_slug.values())

    def get_by_slug(self, slug) -> Movies:
        log.info("получение фильма %s", self.movies_slug.get(slug))
        return self.movies_slug.get(slug)

    def create_movie(self, movie_in: CreateMovies) -> Movies:
        movie = Movies(
            **movie_in.model_dump(),
        )
        self.movies_slug[movie.slug] = movie
        log.info("Making a new film = %s", movie.slug)
        self.save_movie()
        return movie

    def delete_by_slug(self, slug) -> None:
        self.movies_slug.pop(slug)
        self.save_movie()

    def delete(self, movie: Movies) -> None:
        self.delete_by_slug(slug=movie.slug)
        self.save_movie()

    def update_movie(
        self,
        movie: Movies,
        movie_data_in: UpdateMovies,
    ) -> Movies:
        for k, v in movie_data_in:
            setattr(movie, k, v)
        self.save_movie()
        return movie

    def movie_partial_update(
        self,
        movies: Movies,
        movies_in: MoviesPartialUpdate,
    ) -> Movies:
        for field_mane, value in movies_in.model_dump(exclude_unset=True).items():
            setattr(movies, field_mane, value)
        self.save_movie()
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
