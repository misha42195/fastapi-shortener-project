from pydantic import BaseModel


class ShortenedUrlBase(BaseModel):
    target_url: str
    slug: str


class ShortenedUrl(ShortenedUrlBase):
    """Модель сокращенной ссылки"""

    pass
