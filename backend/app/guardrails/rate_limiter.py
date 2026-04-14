import time
from collections.abc import AsyncIterator

import structlog
from fastapi import HTTPException, Request

from app.config import settings

logger = structlog.get_logger()

# In-memory rate limit store (use Redis in production for multi-process)
_rate_store: dict[str, list[float]] = {}


async def check_rate_limit(request: Request) -> AsyncIterator[None]:
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    window = 60.0

    if client_ip not in _rate_store:
        _rate_store[client_ip] = []

    # Remove expired timestamps
    _rate_store[client_ip] = [
        ts for ts in _rate_store[client_ip] if now - ts < window
    ]

    if len(_rate_store[client_ip]) >= settings.rate_limit_per_minute:
        logger.warning("Rate limit exceeded", client_ip=client_ip)
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later.",
            headers={"Retry-After": "60"},
        )

    _rate_store[client_ip].append(now)
    yield  # type: ignore[misc]
