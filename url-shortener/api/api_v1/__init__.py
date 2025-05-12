from fastapi import APIRouter

from api.api_v1.movies.views import router as short_views_router

router = APIRouter(
    prefix="/v1",
)
router.include_router(short_views_router)
