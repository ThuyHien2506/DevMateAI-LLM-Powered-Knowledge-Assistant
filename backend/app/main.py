from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import logger
from app.api.routes import health, chat, search


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="DevMate AI — Evaluated Hybrid & Agentic RAG System for Technical Documentation",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Cấu hình CORS để Frontend React gọi được API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Đăng ký các router
    app.include_router(health.router)
    app.include_router(chat.router, prefix="/api/v1")
    app.include_router(search.router, prefix="/api/v1")

    @app.on_event("startup")
    async def startup_event():
        logger.info(f"DevMate AI Backend is starting up on {settings.HOST}:{settings.PORT}")

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
