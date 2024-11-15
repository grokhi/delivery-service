import httpx
from src.core.logger import logger
from src.core.cache import redis
from src.core.config import settings


async def update_currency_rate():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(settings.CURRENCY_API_URL)
            data = response.json()
            rate = data["rates"]["RUB"]
            await redis.set("currency_rate", str(rate))
            logger.info(f"Updated currency rate: {rate}")
            return rate
    except Exception as e:
        logger.error(f"Failed to update currency rate: {e}")
        return None
