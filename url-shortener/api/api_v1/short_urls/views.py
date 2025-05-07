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


@router.post(
    "/",
    response_model=ShortenedUrl,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    target_url: Annotated[AnyHttpUrl, Form()],
    slug: Annotated[
        str,
        Len(min_length=3, max_length=5),
        Form(),
    ],
):
    return ShortenedUrl(
        target_url=target_url,
        slug=slug,
    )
