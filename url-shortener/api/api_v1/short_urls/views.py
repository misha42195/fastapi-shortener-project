from typing import Annotated
from annotated_types import Len
from pydantic import AnyHttpUrl
from fastapi import (
    Depends,
    APIRouter,
    status,
    Form,
)

from api.api_v1.short_urls.dependecies import (
    prefetch_short_url,
)
from schemas.short_url import (
    ShortenedUrl,
    ShortenedUrlCreated,
)
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


@router.post(
    "/",
    response_model=ShortenedUrl,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(short_url: ShortenedUrlCreated) -> ShortenedUrl:
    return ShortenedUrl(
        **short_url.model_dump(),
    )
