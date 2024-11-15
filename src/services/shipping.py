import json
from typing import Any, Dict, List

from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.models.parcels import Parcel
from src.utils.utils import calculate_shipping_cost


async def handle_shipping_cost(db: AsyncSession, redis: Redis):
    try:
        currency_data = await redis.get("currency_usd")
        if not currency_data:
            print("Currency data not found in Redis.")
            return

        currency_usd = json.loads(currency_data)
        usd_to_rub_rate = currency_usd.get("Value")
        if not usd_to_rub_rate:
            print("Invalid currency data.")
            return

        result = await db.execute(select(Parcel).filter(Parcel.shipping_cost_rub == None))
        parcels: List[Parcel] = result.scalars().all()

        if not parcels:
            print("No parcels found with None shipping_cost_rub.")
            return

        for parcel in parcels:
            parcel.shipping_cost_rub = calculate_shipping_cost(parcel, usd_to_rub_rate)

        await db.commit()
        print(f"Updated {len(parcels)} parcels with calculated shipping costs.")

    except Exception as e:
        await db.rollback()
        print(f"Error handling shipping cost: {e!r}")
