import datetime as dt
import json
from typing import Any, Dict, List

from aioredis import Redis
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import UpdateOne
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.config import settings
from src.core.logger import logger
from src.db.models.parcels import Parcel, ShippingCostRubAgg
from src.resources import strings
from src.utils.utils import calculate_shipping_cost

BATCH_SIZE = 1000


async def handle_shipping_cost(db: AsyncSession, redis: Redis, collection: AsyncIOMotorCollection):
    try:
        currency_data = await redis.get("currency_usd")
        if not currency_data:
            logger.warning(strings.WARN_REDIS_NOT_FOUND)
            return

        currency_usd = json.loads(currency_data)
        usd_to_rub_rate = currency_usd.get("Value")
        if not usd_to_rub_rate:
            logger.error(strings.WARN_INVALID_CURRENCY_DATA)
            return

        result = await db.execute(select(Parcel).filter(Parcel.shipping_cost_rub == None))
        parcels: List[Parcel] = result.scalars().all()

        if not parcels:
            logger.info(strings.LOG_NO_UNREGISTERED_PARCELS)
            return

        for i in range(0, len(parcels), BATCH_SIZE):
            utc_now = dt.datetime.now(dt.timezone.utc)
            batch = parcels[i : i + BATCH_SIZE]
            updates = []
            for parcel in batch:
                parcel.shipping_cost_rub = calculate_shipping_cost(parcel, usd_to_rub_rate)
                updates.append(
                    UpdateOne(
                        {"parcel_id": parcel.id},
                        {
                            "$set": {
                                "parcel_id": parcel.id,
                                "type_id": parcel.type_id,
                                "type": parcel.type,
                                "shipping_cost_rub": parcel.shipping_cost_rub,
                                "timestamp": utc_now,
                                "expireAt": utc_now + dt.timedelta(days=settings.MONGO_EXPIRE_AT),
                            }
                        },
                        upsert=True,
                    )
                )
            if updates:
                res = await collection.bulk_write(updates)
                n_batch = i // BATCH_SIZE + 1
                logger.debug(
                    strings.LOG_DEBUG_SHIPPING_COST_BATCHES.format(
                        n_batch=n_batch,
                        matched_count=res.matched_count,
                        modified_count=res.modified_count,
                    )
                )

        await db.commit()
        logger.info(strings.LOG_SHIPPING_AGG_UPDATE.format(count=len(parcels)))

    except Exception as e:
        await db.rollback()
        logger.error(strings.ERR_SHIPPING_CALC.format(error=str(e)))
        raise


async def aggregate_shipping_costs_by_type_and_day(
    db: AsyncSession, collection: AsyncIOMotorCollection
):
    pipeline = [
        {
            "$group": {
                "_id": {
                    "type": "$type",
                    "type_id": "$type_id",
                    "day": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
                },
                "total_cost": {"$sum": "$shipping_cost_rub"},
            }
        },
        {"$sort": {"_id.day": 1}},
    ]

    try:
        cnt = 0
        async for result in collection.aggregate(pipeline):
            cnt += 1
            logger.debug(strings.LOG_DEBUG_SHIPPING_COSTS_AGG_RESULT.format(result=result))

            ts_str = result["_id"]["day"]
            type_id = result["_id"]["type_id"]
            ts = dt.datetime.strptime(ts_str, "%Y-%m-%d")

            new_agg = ShippingCostRubAgg(
                id=f"{ts_str}_{type_id}",
                timestamp=ts,
                type_id=type_id,
                type=result["_id"]["type"],
                shipping_cost_rub=result["total_cost"],
            )
            await db.merge(new_agg)

        await db.commit()
        logger.info(strings.LOG_SHIPPING_AGG_UPDATE.format(count=cnt))

    except Exception as e:
        await db.rollback()
        logger.error(strings.ERR_SHIPPING_CALC.format(error=str(e)))
        raise
