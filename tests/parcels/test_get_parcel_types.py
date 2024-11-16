import pytest
from fastapi import status
from httpx import AsyncClient

from src.main import app


@pytest.mark.asyncio
async def test_get_parcel_types():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/api/parcels/types")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
