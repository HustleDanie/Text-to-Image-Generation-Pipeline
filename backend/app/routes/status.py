import json

import structlog
from fastapi import APIRouter, HTTPException

from app.schemas.responses import StatusResponse
from app.workers.broker import broker

router = APIRouter()
logger = structlog.get_logger()


@router.get(
    "/status/{job_id}",
    response_model=StatusResponse,
    summary="Check the status of a generation job",
)
async def get_job_status(job_id: str) -> StatusResponse:
    raw = await broker.redis.get(f"job:{job_id}")
    if raw is None:
        raise HTTPException(status_code=404, detail="Job not found")

    data = json.loads(raw)
    image_url = None
    if data.get("status") == "completed":
        image_url = f"/api/images/{job_id}"

    return StatusResponse(
        job_id=job_id,
        status=data["status"],
        progress=data.get("progress"),
        image_url=image_url,
        error=data.get("error"),
    )
