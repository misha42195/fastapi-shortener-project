from datetime import date

from pydantic import BaseModel


# схема для представления фильма
class Movies(BaseModel):
    id: int
    title: str
    description: str
    release_year: date
    director: str
