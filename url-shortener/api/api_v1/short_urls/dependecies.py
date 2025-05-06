from datetime import date

from fastapi import HTTPException
from starlette import status

from schemas.muvies import Movies
from schemas.short_url import ShortenedUrl

SHORT_URL = [
    ShortenedUrl(
        target_url="https://www.example.com",
        slug="example",
    ),
    ShortenedUrl(
        target_url="https://www.google.com",
        slug="search",
    ),
]
movies_list: list[Movies] = [
    Movies(
        id=1,
        title="Побег из Шоушенка",
        description="Два заключённых сближаются за годы заключения, находя утешение и надежду на свободу.",
        release_year=date(1994, 9, 22),
        director="Фрэнк Дарабонт",
    ),
    Movies(
        id=2,
        title="Крёстный отец",
        description="Стареющий глава мафиозной семьи передаёт власть своему неохотному сыну.",
        release_year=date(1972, 3, 24),
        director="Фрэнсис Форд Коппола",
    ),
    Movies(
        id=3,
        title="Начало",
        description="Вор использует технологию проникновения в сны, чтобы внедрить идею в сознание цели.",
        release_year=date(2010, 7, 16),
        director="Кристофер Нолан",
    ),
    Movies(
        id=4,
        title="Паразиты",
        description="Бедная семья внедряется в жизнь богатой семьи, что приводит к неожиданным последствиям.",
        release_year=date(2019, 5, 30),
        director="Пон Чжун Хо",
    ),
    Movies(
        id=5,
        title="Матрица",
        description="Хакер узнаёт правду о своей реальности и борется с контролирующей её системой.",
        release_year=date(1999, 3, 31),
        director="Лана и Лилли Вачовски",
    ),
]


def prefetch_short_url(slug: str) -> ShortenedUrl:
    url: ShortenedUrl | None = next(
        (url for url in SHORT_URL if url.slug == slug), None
    )
    if url:
        return url

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )


def prefetch_movie(movie_id: int) -> Movies:
    movie: Movies | None = next(
        (movie for movie in movies_list if movie.id == movie_id), None
    )
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {movie_id} not found",
    )
