import json
from typing import Any, Dict, List

import httpx
from aioredis import Redis

from src.core.config import settings


async def fetch_currency_data(redis: Redis):
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
