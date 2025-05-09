from annotated_types import Len
from pydantic import BaseModel, AnyHttpUrl
from typing import Annotated


class ShortenedUrlBase(BaseModel):
    target_url: AnyHttpUrl
    slug: str


class ShortenedUrl(ShortenedUrlBase):
    """Модель сокращенной ссылки"""

    pass


class ShortenedUrlCreated(ShortenedUrlBase):
    """
    Модель для создания сокращенной ссылки
    """

    slug: Annotated[str, Len(3, 5)]
