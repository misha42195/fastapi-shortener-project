from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
def get_root(
    request: Request,
    name: str = "World",
) -> dict[str, str]:  # = "World",
    docs_path = str(
        request.url.replace(
            path="/docs",
            query="",
        ),
    )

    return {
        "message": f"Hello {name}",
        "docs_path": docs_path,
    }
