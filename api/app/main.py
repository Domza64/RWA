import logging

from fastapi import FastAPI

from app.core.config import settings
from app.core.errors import AppError, app_error_handler
from app.core.logging import setup_logging
from app.routers.health import router as health_router

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    App factory — kreira, konfigurira i vraća FastAPI instancu.
    """
    # Konfiguracija logiranja
    setup_logging()

    # FastAPI instanca.
    app = FastAPI(
        title="Jira 2",
        version="0.1.0",
        description="Sustav za pračenje zadataka u timu.",
        docs_url="/docs" if settings.ENV == "dev" else None,
        redoc_url=None,
    )

    # Globalni exception handler za AppError
    app.add_exception_handler(AppError, app_error_handler)

    # 4. Uključivanje routera.
    #    prefix="/health" znači: svi endpointi iz health routera
    #    dobivaju prefix, pa @router.get("/") postaje GET /health.
    app.include_router(health_router, prefix="/health", tags=["health"])

    logger.info("Aplikacija kreirana (env=%s)", settings.ENV)
    return app


# Uvicorn traži ovu varijablu: uvicorn app.main:app
# Poziva create_app() jednom pri startu servera.
app = create_app()
