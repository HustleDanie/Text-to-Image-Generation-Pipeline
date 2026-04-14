from collections.abc import AsyncIterator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def mock_broker() -> MagicMock:
    with patch("app.routes.generate.broker") as mock:
        mock.redis = AsyncMock()
        mock.redis.set = AsyncMock()
        mock.redis.get = AsyncMock()
        yield mock


@pytest.fixture
def mock_generate_task() -> MagicMock:
    with patch("app.routes.generate.generate_image") as mock:
        mock.kiq = AsyncMock()
        yield mock


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
