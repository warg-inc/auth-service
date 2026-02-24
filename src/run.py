from src.setup.app_factory import create_web_app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.setup.app_factory:create_web_app",
        factory=True,
        host="0.0.0.0",
        port=8001,
        reload=True,
        reload_dirs=["src"],
    )