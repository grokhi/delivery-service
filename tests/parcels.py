import asyncio

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.config import settings
from src.db.base import Base
from src.db.models.parcels import Parcel, ParcelType
from src.main import app
from src.resources import strings


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


@pytest.mark.asyncio
async def test_get_parcel_types():
    # Remove base_url to avoid middleware issues
    async with AsyncClient(app=app) as ac:
        response = await ac.get("/api/parcels/types")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_parcel_types():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/api/parcels/types")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)


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


@pytest.mark.asyncio
async def test_get_parcels_list():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/api/parcels/list")
        assert response.status_code == status.HTTP_200_OK
        assert "parcels" in response.json()
        assert "total_count" in response.json()
        assert isinstance(response.json()["parcels"], list)
