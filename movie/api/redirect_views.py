
from fastapi import APIRouter

router = APIRouter(
    prefix="/r",
    tags=["Redirect"],
)


# @router.get("/{slug}")
# @router.get("/{slug}/")
# def redirect_short_url(
#     url: Annotated[
#         ShortenedUrl,
#         Depends(prefetch_short_url),
#     ],
# ):
#     return RedirectResponse(
#         url=url.target_url,
#     )
