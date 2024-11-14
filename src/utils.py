from __future__ import annotations

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import json
from redis import Redis
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.parcels import models
import httpx
import asyncio
import aioredis
from typing import Any, Dict, TYPE_CHECKING
import json

if TYPE_CHECKING:
    from .parcels.schemas import Parcel, ParcelType, ParcelCreate


SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+mysqlconnector://root:@localhost/database"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Gets a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


def get_parcel_type(name: str, db: Session) -> models.ParcelType:
    type_record = db.query(models.ParcelType).filter_by(name=name).first()
    if not type_record:
        raise HTTPException(
            status_code=400, detail=f"Parcel type '{name}' not found in the database."
        )
    return type_record
