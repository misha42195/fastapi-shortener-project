from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from schemas.muvies import UpdateMovies
from services.movies import FormResponseHelper

router = APIRouter(
    prefix="/{slug}/update",
)
response_helper = FormResponseHelper(
    model=UpdateMovies,
    template_name="movies/update.html",
)


@router.get(
    path="/",
    name="movie:update-views",
    response_model=None,
)
def get_page_update_view(
    request: Request,
) -> HTMLResponse:
    return response_helper.create_view_validation_response(request=request)
