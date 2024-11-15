from __future__ import annotations

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import json
from redis import Redis
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.db.models.parcels import Parcel, ParcelType
from src.schemas.parcels import ParcelCreate
import httpx
import asyncio
import aioredis
from typing import Any, Dict, TYPE_CHECKING
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# if TYPE_CHECKING:
#     from .schemas.parcels import Parcel, ParcelType, ParcelCreate


def calculate_shipping_cost(parcel: ParcelCreate, exchange_rate: float):
    """Calculates the shipping cost for a parcel."""
    return (parcel.weight * 0.5 + parcel.cost_usd * 0.01) * exchange_rate


def get_exchange_rate(redis: Redis):
    """Retrieves the exchange rate from Redis."""
    exchange_rate = redis.get("exchange_rate", encoding="utf-8")
    if exchange_rate:
        return float(exchange_rate)
    else:
        # Load from file if not in cache
        with open("currencies_json.js", "r") as f:
            exchange_rate_data = json.load(f)
            exchange_rate = exchange_rate_data["RUB"]
            redis.set("exchange_rate", exchange_rate)
        return exchange_rate


def generate_uuid() -> str:
    return str(uuid.uuid4())


async def get_parcel_type(name: str, db: AsyncSession) -> ParcelType:
    # type_record = db.query(ParcelType).filter_by(name=name).first()
    result = await db.execute(select(ParcelType).filter_by(name=name))
    type_record = result.scalar()
    if not type_record:
        raise HTTPException(
            status_code=400, detail=f"Parcel type '{name}' not found in the database."
        )
    return type_record
