from datetime import date
from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel


# схема для представления фильма
class Movies(BaseModel):
    slug: Annotated[str, Len(3, 10)]
    title: str
    description: str
    release_year: date
    director: str


class CreateMovie(Movies):
    """
    Модель для создания объектов фильмов
    """

    slug: Annotated[
        str,
        Len(3, 10),
    ]
