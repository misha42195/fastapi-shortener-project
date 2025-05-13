from datetime import date

from pydantic import BaseModel

from schemas.muvies import (
    Movies,
    CreateMovie,
    UpdateMovie,
)


class MoviesStorage(BaseModel):
    movies_slug: dict[str, Movies] = {}

    def get_movies(self) -> list[Movies]:
        return list(self.movies_slug.values())

    def get_by_slug(self, slug) -> Movies:
        return self.movies_slug.get(slug)

    def create_movie(self, movie_in: CreateMovie) -> Movies:
        movie = Movies(
            **movie_in.model_dump(),
        )
        self.movies_slug[movie.slug] = movie
        return movie

    def delete_by_slug(self, slug) -> None:
        self.movies_slug.pop(slug)

    def delete(self, movie: Movies) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update_movie(
        self,
        movie: Movies,
        movie_data_in: UpdateMovie,
    ) -> Movies:
        # new_movie = movie.model_copy(
        #     update=movie_data_in.model_dump(),
        # )
        # self.movies_slug[new_movie.slug] = new_movie
        for k, v in movie_data_in:
            setattr(movie, k, v)
        return movie


movie_storage = MoviesStorage()

movie_storage.create_movie(
    CreateMovie(
        slug="shoushenka",
        title="Побег из Шоушенка",
        description="Два заключённых сближаются за годы заключения, находя утешение и надежду на свободу.",
        release_year=date(1994, 9, 22),
        director="Фрэнк Дарабонт",
    )
)
movie_storage.create_movie(
    CreateMovie(
        slug="father",
        title="Крёстный отец",
        description="Стареющий глава мафиозной семьи передаёт власть своему неохотному сыну.",
        release_year=date(1972, 3, 24),
        director="Фрэнсис Форд Коппола",
    )
)
movie_storage.create_movie(
    CreateMovie(
        slug="start",
        title="Начало",
        description="Вор использует технологию проникновения в сны, чтобы внедрить идею в сознание цели.",
        release_year=date(2010, 7, 16),
        director="Кристофер Нолан",
    ),
)
