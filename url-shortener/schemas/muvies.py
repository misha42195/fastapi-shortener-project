from datetime import date
from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import BaseModel


# схема для представления фильма
class MoviesBase(BaseModel):
    """
    Базовая модель
    """

    title: str
    description: Annotated[
        str,
        MaxLen(150),
    ] = ""
    release_year: date
    director: str


class Movies(MoviesBase):
    """
    Модель для валидации фильма
    """

    slug: str


class CreateMovie(MoviesBase):
    """
    Модель для создания фильма
    """

    slug: Annotated[
        str,
        Len(3, 10),
    ]


class UpdateMovie(MoviesBase):
    """
    Модель для обновления фильма
    """

    description: str
