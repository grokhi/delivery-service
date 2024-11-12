from fastapi import FastAPI
from src.redis import Redis
from .utils import calculate_shipping_cost, get_exchange_rate
from .database import engine, SessionLocal
from .parcels.schemas import Parcel

import asyncio
import time
from datetime import timedelta


async def schedule_shipping_cost_calculation(redis: Redis):
    """Schedules the shipping cost calculation task."""
    while True:
        await calculate_shipping_costs(redis)
        await asyncio.sleep(300)  # Run every 5 minutes (300 seconds)


async def calculate_shipping_costs(redis: Redis):
    """Calculates shipping costs for unprocessed parcels."""
    db = SessionLocal()
    try:
        exchange_rate = get_exchange_rate(redis)
        unprocessed_parcels = db.query(Parcel).filter(Parcel.shipping_cost.is_(None)).all()
        for parcel in unprocessed_parcels:
            shipping_cost = calculate_shipping_cost(parcel, exchange_rate)
            parcel.shipping_cost = shipping_cost
            db.commit()
            db.refresh(parcel)
            redis.hset(f"parcel:{parcel.id}:shipping_cost", shipping_cost)
    finally:
        db.close()
