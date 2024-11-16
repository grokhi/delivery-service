import pytest
from fastapi import status
from httpx import AsyncClient

from src.main import app


@pytest.mark.asyncio
async def test_create_parcel():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post(
            "api/parcels/create",
            json={
                "name": "Test Parcel",
                "weight": 2.5,
                "type": "clothing",
                "cost_usd": 10.0,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert "parcel_id" in response.json()
