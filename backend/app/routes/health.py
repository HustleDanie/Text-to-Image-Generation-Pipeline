from fastapi import APIRouter

from app.config import settings
from app.schemas.responses import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, summary="Health check")
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        model_loaded=False,
        device=settings.device,
        version="0.1.0",
    )
