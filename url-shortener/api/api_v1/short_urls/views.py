from typing import Annotated

from fastapi import Depends, APIRouter

from api.api_v1.short_urls.dependecies import (
    prefetch_short_url,
)
from schemas.short_url import ShortenedUrl
from api.api_v1.short_urls.dependecies import SHORT_URL

router = APIRouter(
    prefix="/short-urls",
    tags=["ShortURLs"],
)


@router.get("/", response_model=list[ShortenedUrl])
def read_short_url():
    return SHORT_URL


@router.get(
    "/{slug}",
    response_model=ShortenedUrl,
)
def read_short_url_details(
    url: Annotated[
        ShortenedUrl,
        Depends(prefetch_short_url),
    ],
) -> ShortenedUrl:
    return url
