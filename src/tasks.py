from fastapi import FastAPI
from .utils import calculate_shipping_cost, get_exchange_rate, get_db
from .parcels.schemas import Parcel

import asyncio
import time
from datetime import timedelta
import aioredis
from typing import Any, Dict, List
import json
import httpx
import asyncio
from sqlalchemy.orm import Session
from src.parcels import models

CURRENCY_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
UPDATE_INTERVAL = 300  # sec


REDIS_URL = "redis://localhost:6379"


async def get_redis() -> aioredis.Redis:
    return await aioredis.from_url(REDIS_URL, decode_responses=True)


async def fetch_currency_data(redis: aioredis.Redis):
    async with httpx.AsyncClient() as client:
        response = await client.get(CURRENCY_URL)
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


async def handle_shipping_cost(db: Session, redis: aioredis.Redis):
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
        parcels: List[models.Parcel] = (
            db.query(models.Parcel).filter(models.Parcel.shipping_cost_rub == None).all()
        )

        if not parcels:
            print("No parcels found with None shipping_cost_rub.")
            return

        for parcel in parcels:
            parcel.shipping_cost_rub = calculate_shipping_cost(parcel, usd_to_rub_rate)

        db.commit()
        print(f"Updated {len(parcels)} parcels with calculated shipping costs.")

    except Exception as e:
        db.rollback()
        print(f"Error handling shipping cost: {e}")


async def schedule_currency_update():
    redis = await get_redis()
    db = next(get_db())
    while True:
        await fetch_currency_data(redis)
        await handle_shipping_cost(db, redis)
        await asyncio.sleep(UPDATE_INTERVAL)
