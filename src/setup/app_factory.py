from fastapi import(
    FastAPI,
    APIRouter,
)

from src.presentation.http.controllers.root_router import create_root_router


def create_web_app() -> FastAPI:
    app = FastAPI()
    app.include_router(create_root_router())

    return app