import pytest
from fastapi import status
from httpx import AsyncClient

from src.main import app


@pytest.mark.asyncio
async def test_get_parcels_list():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/api/parcels/list")
        assert response.status_code == status.HTTP_200_OK
        assert "parcels" in response.json()
        assert "total_count" in response.json()
        assert isinstance(response.json()["parcels"], list)
