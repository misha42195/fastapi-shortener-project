from fastapi import APIRouter

from rest.movies.list_views import router as list_views_router

router = APIRouter(
    prefix="/movies",
)

router.include_router(list_views_router)
