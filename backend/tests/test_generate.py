import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_generate_returns_202_with_job_id(
    client: AsyncClient,
    mock_broker,
    mock_generate_task,
) -> None:
    # Arrange
    payload = {
        "prompt": "A beautiful sunset over mountains",
        "width": 512,
        "height": 512,
    }

    # Act
    response = await client.post("/api/generate", json=payload)

    # Assert
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "queued"


@pytest.mark.asyncio
async def test_generate_rejects_empty_prompt(client: AsyncClient) -> None:
    # Arrange
    payload = {"prompt": "", "width": 512, "height": 512}

    # Act
    response = await client.post("/api/generate", json=payload)

    # Assert
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_generate_rejects_invalid_dimensions(client: AsyncClient) -> None:
    # Arrange
    payload = {"prompt": "test prompt", "width": 2048, "height": 512}

    # Act
    response = await client.post("/api/generate", json=payload)

    # Assert
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_generate_rejects_extra_fields(client: AsyncClient) -> None:
    # Arrange
    payload = {"prompt": "test prompt", "unknown_field": "value"}

    # Act
    response = await client.post("/api/generate", json=payload)

    # Assert
    assert response.status_code == 422
