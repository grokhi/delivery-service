import json
from typing import Any, Dict, List

from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.logger import logger
from src.db.models.parcels import Parcel
from src.resources import strings
from src.utils.utils import calculate_shipping_cost


async def handle_shipping_cost(db: AsyncSession, redis: Redis):
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

        for parcel in parcels:
            parcel.shipping_cost_rub = calculate_shipping_cost(parcel, usd_to_rub_rate)

        await db.commit()
        logger.info(strings.LOG_SHIPPING_UPDATE.format(count=len(parcels)))

    except Exception as e:
        await db.rollback()
        logger.error(strings.ERR_SHIPPING_CALC.format(error=str(e)))
        raise
