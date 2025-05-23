from datetime import date
from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import BaseModel

DescriptionString = Annotated[
    str,
    MaxLen(100),
]

SlugString = Annotated[
    str,
    Len(3, 10),
]


class MoviesBase(BaseModel):
    """
    Базовая модель
    """

    title: str
    description: DescriptionString = ""
    release_year: date
    director: str


class Movies(MoviesBase):
    """
    Модель для валидации фильма
    """

    slug: str
    notes: str = ""


class MoviesRead(MoviesBase):
    """
    модель для чтения, поля которого отдаем во фронт,
    указаны только разрешенные поля, кроме поля notes
    """

    slug: str


class CreateMovies(MoviesBase):
    """
    Модель для создания фильма
    """

    slug: SlugString


class UpdateMovies(MoviesBase):
    """
    Модель для обновления данных фильма
    """

    description: DescriptionString


class MoviesPartialUpdate(MoviesBase):
    title: str | None = None
    description: DescriptionString | None = None
    release_year: date | None = None
    director: str | None = None
