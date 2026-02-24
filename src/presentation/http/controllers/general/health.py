from fastapi import (
    APIRouter,
    Request,
)


def create_health_router() -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    async def health(_: Request) -> dict[str, str]:
        return {"status": "ok"}

    return router