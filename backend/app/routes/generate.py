import uuid

import structlog
from fastapi import APIRouter, Depends

from app.config import settings
from app.guardrails.prompt_filter import validate_prompt
from app.guardrails.rate_limiter import check_rate_limit
from app.schemas import GenerateRequest
from app.schemas.responses import JobResponse
from app.workers.broker import broker
from app.workers.tasks import generate_image

router = APIRouter()
logger = structlog.get_logger()


@router.post(
    "/generate",
    response_model=JobResponse,
    status_code=202,
    summary="Submit an image generation job",
)
async def create_generation(
    request: GenerateRequest,
    _rate_limit: None = Depends(check_rate_limit),
) -> JobResponse:
    validate_prompt(request.prompt)

    job_id = str(uuid.uuid4())

    await broker.redis.set(
        f"job:{job_id}",
        '{"status": "queued", "progress": 0}',
        ex=3600,
    )

    await generate_image.kiq(
        job_id=job_id,
        prompt=request.prompt,
        negative_prompt=request.negative_prompt,
        width=request.width,
        height=request.height,
        guidance_scale=request.guidance_scale,
        num_inference_steps=request.num_inference_steps,
        seed=request.seed,
        scheduler=request.scheduler,
        lora_model_id=request.lora_model_id,
        lora_scale=request.lora_scale,
    )

    logger.info("Generation job queued", job_id=job_id, prompt=request.prompt[:50])
    return JobResponse(job_id=job_id, status="queued")
