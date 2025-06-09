from typing import Annotated

from annotated_types import Len
from pydantic import AnyHttpUrl, BaseModel


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
