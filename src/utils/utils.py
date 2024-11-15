import json
import uuid

from src.db.models.parcels import Parcel, ParcelType
from src.schemas.parcels import ParcelCreate
import httpx
import asyncio
from aioredis import Redis
from typing import Any, Dict, TYPE_CHECKING
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


def calculate_shipping_cost(parcel: ParcelCreate, exchange_rate: float):
    """Calculates the shipping cost for a parcel."""
    return (parcel.weight * 0.5 + parcel.cost_usd * 0.01) * exchange_rate


def generate_uuid() -> str:
    return str(uuid.uuid4())
