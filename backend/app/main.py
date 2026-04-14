from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import generate, health, images, models, status
from app.utils.errors import register_exception_handlers
from app.utils.logging import configure_logging

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    logger.info(
        "Starting application",
        model_id=settings.model_id,
        device=settings.device,
    )
    yield
    logger.info("Shutting down application")


app = FastAPI(
    title="Text-to-Image Generation API",
    description="Generate images from text prompts with LoRA fine-tuning support",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(health.router, tags=["health"])
app.include_router(generate.router, prefix=settings.api_prefix, tags=["generation"])
app.include_router(status.router, prefix=settings.api_prefix, tags=["status"])
app.include_router(images.router, prefix=settings.api_prefix, tags=["images"])
app.include_router(models.router, prefix=settings.api_prefix, tags=["models"])
