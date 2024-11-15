import asyncio

from src.core.cache import redis
from src.core.config import settings
from src.db.base import get_db
from src.services.currency import fetch_currency_data
from src.services.shipping import handle_shipping_cost


async def schedule_currency_update():
    async for db in get_db():
        while True:
            await fetch_currency_data(redis)
            await handle_shipping_cost(db, redis)
            await asyncio.sleep(settings.UPDATE_INTERVAL)


async def startup_event():
    try:
        asyncio.create_task(schedule_currency_update())
    except Exception as e:
        print(f"Startup failed: {e}")
