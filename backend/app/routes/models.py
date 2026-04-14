from fastapi import APIRouter

from app.config import settings
from app.schemas.responses import ModelInfo, ModelsResponse

router = APIRouter()


@router.get("/models", response_model=ModelsResponse, summary="List available models")
async def list_models() -> ModelsResponse:
    models = [
        ModelInfo(
            model_id=settings.model_id,
            name="Stable Diffusion XL Base",
            model_type="base",
            description="SDXL 1.0 base model for high-quality image generation",
        ),
    ]
    return ModelsResponse(models=models)
