__all__ = ("router",)
from fastapi import APIRouter

from api.api_v1.movies.views import router as movie_views_router

router = APIRouter(
    prefix="/v1",
)
router.include_router(movie_views_router)
