from fastapi import APIRouter

from api.api_v1.short_urls.views import router as short_views_router

router = APIRouter(
    prefix="/v1",
)
router.include_router(short_views_router)
