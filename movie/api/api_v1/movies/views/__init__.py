__all__ = ("router", "movie_storage")

from api.api_v1.movies import movie_storage
from api.api_v1.movies.views.detail_views import router as detail_router
from api.api_v1.movies.views.list_views import router

router.include_router(detail_router)
