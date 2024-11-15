from fastapi import FastAPI
from src.utils.utils import calculate_shipping_cost, get_exchange_rate
from src.db.base import get_db
from src.schemas.parcels import Parcel

import asyncio
import time
from datetime import timedelta
import aioredis
from typing import Any, Dict, List
import json
import httpx
import asyncio
from sqlalchemy.orm import Session
from src.db.models.parcels import Parcel

from redis import asyncio as aioredis
from functools import wraps
from src.core.config import settings

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

redis = aioredis.from_url(settings.REDIS_URL)


def cache_decorator(expire_time=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            cached = await redis.get(cache_key)
            if cached:
                return cached
            result = await func(*args, **kwargs)
            await redis.set(cache_key, result, ex=expire_time)
            return result

        return wrapper

    return decorator


# CURRENCY_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
# UPDATE_INTERVAL = 300  # sec


# REDIS_URL = "redis://localhost:6379"


async def get_redis() -> aioredis.Redis:
    return await aioredis.from_url(settings.REDIS_URL, decode_responses=True)


async def fetch_currency_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.CURRENCY_API_URL)
        if response.status_code == 200:
            currency_data = response.json()
            try:
                currency_usd = currency_data["Valute"]["USD"]
            except KeyError:
                print("URL is broken")
                return
            await redis.set("currency_usd", json.dumps(currency_usd))

            print("Currency data updated in Redis")
        else:
            print(f"Failed to fetch currency data: {response.status_code}")


async def handle_shipping_cost(db: AsyncSession):
    try:
        # Fetch USD to RUB exchange rate from Redis cache
        currency_data = await redis.get("currency_usd")
        if not currency_data:
            print("Currency data not found in Redis.")
            return

        currency_usd = json.loads(currency_data)
        usd_to_rub_rate = currency_usd.get("Value")
        if not usd_to_rub_rate:
            print("Invalid currency data.")
            return

        # Find records with None shipping_cost_rub
        # parcels: List[Parcel] = db.query(Parcel).filter(Parcel.shipping_cost_rub == None).all()
        result = await db.execute(select(Parcel).filter(Parcel.shipping_cost_rub == None))
        parcels = result.scalars().all()

        if not parcels:
            print("No parcels found with None shipping_cost_rub.")
            return

        for parcel in parcels:
            parcel.shipping_cost_rub = calculate_shipping_cost(parcel, usd_to_rub_rate)

        await db.commit()
        print(f"Updated {len(parcels)} parcels with calculated shipping costs.")

    except Exception as e:
        db.rollback()
        print(f"Error handling shipping cost: {e}")


async def schedule_currency_update():
    # redis = await get_redis()
    # db = next(get_db())
    async for db in get_db():
        while True:
            await fetch_currency_data()
            await handle_shipping_cost(db)
            await asyncio.sleep(settings.UPDATE_INTERVAL)
