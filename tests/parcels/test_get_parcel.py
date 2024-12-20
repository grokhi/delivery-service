import pytest
from fastapi import status
from httpx import AsyncClient

from src.main import app


@pytest.mark.asyncio
async def test_get_parcel():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        create_response = await ac.post(
            "api/parcels/create",
            json={
                "name": "Test Parcel",
                "weight": 1,
                "type": "clothing",
                "cost_usd": 1,
            },
        )
        print(create_response.json())
        parcel_id = create_response.json()["parcel_id"]

        response = await ac.get(f"/api/parcels/{parcel_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["weight"] == 1
        assert response.json()["type"] == "clothing"
        assert response.json()["cost_usd"] == 1
        cost = response.json()["shipping_cost_rub"]
        assert cost == "Not calculated yet." or cost > 0
