import json
from typing import Any, Dict, List

import httpx
from aioredis import Redis

from src.core.config import settings
from src.core.logger import logger
from src.resources import strings


async def fetch_currency_data(redis: Redis):
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
            response = await client.get(settings.CURRENCY_API_URL)
            if response.status_code == 200:
                currency_data = response.json()
                currency_usd = currency_data["Valute"]["USD"]
                await redis.set("currency_usd", json.dumps(currency_usd))
                logger.info(strings.LOG_CURRENCY_UPDATE)
            else:
                logger.error(strings.ERR_CURRENCY_FETCH.format(status_code=response.status_code))

    except Exception as e:
        logger.error(strings.ERR_CURRENCY_PARSE.format(error=str(e)))
        raise
