import asyncio

from src.core.cache import redis
from src.core.config import settings
from src.core.logger import logger
from src.db.base import get_db
from src.resources import strings
from src.services.currency import fetch_currency_data
from src.services.shipping import handle_shipping_cost


async def schedule_currency_update():
    async for db in get_db():
        while True:
            await fetch_currency_data(redis)
            await handle_shipping_cost(db, redis)
            await asyncio.sleep(settings.UPDATE_INTERVAL)


async def run_debug_events(event_name: str = "all"):
    """
    Run specific tasks manually for debugging purposes.

    Args:
        task_name (str): Name of the task to run ("currency", "shipping", or "all")
    """

    try:
        if event_name in ["currency", "all"]:
            logger.debug(strings.LOG_DEBUG_FETCH_CURRENCY)
            await fetch_currency_data(redis)

        if event_name in ["shipping", "all"]:
            logger.debug(strings.LOG_DEBUG_SHIPPING_COST)
            async for db in get_db():
                await handle_shipping_cost(db, redis)

    except Exception as e:
        logger.error(f"Error during debug task execution: {e}")
        raise e


async def startup_event():
    try:
        asyncio.create_task(schedule_currency_update())
    except Exception as e:
        logger.error(strings.ERR_STARTUP_FAILED.format(error=str(e)))
