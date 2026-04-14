from pathlib import Path

import structlog
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.config import settings

router = APIRouter()
logger = structlog.get_logger()


@router.get(
    "/images/{job_id}",
    summary="Retrieve a generated image",
    responses={200: {"content": {"image/png": {}}}},
)
async def get_image(job_id: str) -> FileResponse:
    safe_job_id = Path(job_id).name
    if safe_job_id != job_id or "/" in job_id or "\\" in job_id:
        raise HTTPException(status_code=400, detail="Invalid job ID")

    image_path = Path(settings.storage_path) / f"{safe_job_id}.png"
    if not image_path.is_file():
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(
        path=str(image_path),
        media_type="image/png",
        filename=f"{safe_job_id}.png",
    )
