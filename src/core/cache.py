import aioredis
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import settings

redis = aioredis.from_url(settings.REDIS_URL)


mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
db = mongo_client["delivery_service"]
collection = db["shipping_logs"]


async def create_indexes():
    indexes = await collection.index_information()
    if "expireAt_1" not in indexes:
        await collection.create_index("expireAt", expireAfterSeconds=0)
