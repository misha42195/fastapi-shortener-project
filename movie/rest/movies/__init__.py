from fastapi import APIRouter, Depends

from dependencies.auth import user_basic_auth_required_for_unsafe_methods
from rest.movies.create_views import router as create_views_router
from rest.movies.list_views import router as list_views_router

router = APIRouter(
    prefix="/movies",
    tags=["Create Movie REST"],
    dependencies=[
        Depends(user_basic_auth_required_for_unsafe_methods),
    ],
)

router.include_router(list_views_router)
router.include_router(create_views_router)
