from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from api.api_v1.short_urls.dependecies import prefetch_short_url
from schemas.short_url import ShortenedUrl

router = APIRouter(
    prefix="/r",
    tags=["Redirect"],
)


@router.get("/{slug}")
@router.get("/{slug}/")
def redirect_short_url(
    url: Annotated[
        ShortenedUrl,
        Depends(prefetch_short_url),
    ],
):
    return RedirectResponse(
        url=url.target_url,
    )
