from pathlib import Path

import structlog

from app.config import settings

logger = structlog.get_logger()


def ensure_storage_dir() -> Path:
    path = Path(settings.storage_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_image(job_id: str, image_data: bytes) -> Path:
    storage_dir = ensure_storage_dir()

    safe_name = Path(job_id).name
    file_path = storage_dir / f"{safe_name}.png"

    file_path.write_bytes(image_data)
    logger.info("Image saved", job_id=job_id, path=str(file_path))
    return file_path


def get_image_path(job_id: str) -> Path | None:
    safe_name = Path(job_id).name
    file_path = Path(settings.storage_path) / f"{safe_name}.png"

    if file_path.is_file():
        return file_path
    return None


def delete_image(job_id: str) -> bool:
    path = get_image_path(job_id)
    if path is not None:
        path.unlink()
        logger.info("Image deleted", job_id=job_id)
        return True
    return False
