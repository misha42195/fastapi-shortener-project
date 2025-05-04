from datetime import date
from typing import Annotated
from fastapi import (
    FastAPI,
    Request,
    status,
    HTTPException,
    Depends,
)
from fastapi.responses import (
    RedirectResponse,
)

from schemas.short_url import ShortenedUrl
from schemas.muvies import Movies

app = FastAPI(title="URL Shortener")


@app.get("/")
def get_root(request: Request, name: str = "World"):
    docs_path = str(
        request.url.replace(
            path="/docs",
            query="",
        )
    )

    return {
        "message": f"Hello {name}",
        "docs_path": docs_path,
    }


# список из объектов
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


@app.get(
    "/short-urls/",
    response_model=list[ShortenedUrl],
)
def get_short_urls():
    return SHORT_URL


# функция, которая возвращает или url,
# если есть полное совпадение или ошибку
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


@app.get("/r/{slug}")
@app.get("/r/{slug}/")
def redirect_short_url(
    url: Annotated[
        ShortenedUrl,
        Depends(prefetch_short_url),
    ],
):
    return RedirectResponse(
        url=url.target_url,
    )


@app.get(
    "/short-urls/{slug}",
    response_model=ShortenedUrl,
)
def read_short_url_details(
    url: Annotated[
        ShortenedUrl,
        Depends(prefetch_short_url),
    ],
) -> ShortenedUrl:
    return url


# список фильмов для отображения их на сайте

movies_list = [
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


@app.get(
    "/films/",
    response_model=list[Movies],
)
def get_movies():
    return movies_list


def prefetch_movie(movie_id: int) -> Movies | HTTPException:
    movie: Movies | None = next(
        (movie for movie in movies_list if movie.id == movie_id), None
    )
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {movie_id} not found",
    )


@app.get(
    "/films/{movie_id}/",
    response_model=Movies,
)
def get_movie(
    movie: Annotated[
        Movies,
        Depends(prefetch_movie),
    ],
) -> Movies:
    return movie
