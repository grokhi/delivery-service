import aioredis

from src.core.config import settings

redis = aioredis.from_url(settings.REDIS_URL)


async def get_redis() -> aioredis.Redis:
    return await aioredis.from_url(settings.REDIS_URL, decode_responses=True)
