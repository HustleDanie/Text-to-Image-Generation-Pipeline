import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_returns_200(client: AsyncClient) -> None:
    # Act
    response = await client.get("/health")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "device" in data


@pytest.mark.asyncio
async def test_health_contains_model_status(client: AsyncClient) -> None:
    # Act
    response = await client.get("/health")

    # Assert
    data = response.json()
    assert "model_loaded" in data
