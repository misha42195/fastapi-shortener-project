from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from dependencies.movies import (
    GetMovieStorage,
    MovieBySlug,
)
from schemas.muvies import Movies
from services.movies import FormResponseHelper

router = APIRouter(
    prefix="/{slug}/delete",
)

response_helper = FormResponseHelper(
    model=Movies,
    template_name="movies/delete",
)


# @router.get(
#     path="/",
#     name="movies:delete-view",
#     response_model=None,
# )
# def get_page_delete_view(
#     request: Request,
#     movie: MovieBySlug,
# ) -> HTMLResponse:
#     context: dict[str, Any] = {}
#     context.update(movies=movie)
#     return templates.TemplateResponse(
#         request=request,
#         name="movies/delete.html",
#         status_code=status.HTTP_200_OK,
#         context=context,
#     )


@router.delete(
    path="/",
    name="delete:movie",
)
def delete_movie(
    request: Request,
    movie: MovieBySlug,
    storage: GetMovieStorage,
) -> Response:
    storage.delete(movie=movie)

    return Response(
        content="",
        status_code=status.HTTP_200_OK,
    )
