from typing import Any

from fastapi import (
    APIRouter,
    Request,
)
from fastapi.responses import HTMLResponse

from templating import templates

router = APIRouter(
    include_in_schema=False,
)

movies = [
    "фильм 2020",
    "фильм 2021",
    "фильм 2022",
    "фильм 2023",
    "фильм 2024",
]


@router.get(
    path="/",
    name="home",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def home_page(request: Request) -> HTMLResponse:
    context: dict[str, Any] = {}
    context.update(
        movies=movies,
    )
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=context,
    )


@router.get(
    path="/about/",
    name="about",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def about_page(
    request: Request,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="about.html",
    )
