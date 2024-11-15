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


async def run_debug_tasks(task_name: str = "all"):
    """
    Run specific tasks manually for debugging purposes.

    Args:
        task_name (str): Name of the task to run ("currency", "shipping", or "all")
    """
    # logger.info(f"Running debug task: {task_name}")

    try:
        if task_name in ["currency", "all"]:
            # logger.debug("Running currency fetch task")
            await fetch_currency_data(redis)

        if task_name in ["shipping", "all"]:
            # logger.debug("Running shipping cost calculation task")
            async for db in get_db():
                await handle_shipping_cost(db, redis)

        # logger.info("Debug tasks completed successfully")

    except Exception as e:
        # logger.error(f"Error during debug task execution: {e}")
        raise


async def startup_event():
    try:
        asyncio.create_task(schedule_currency_update())
    except Exception as e:
        print(f"Startup failed: {e}")
