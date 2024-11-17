from fastapi import APIRouter, Response

from src.core.config import settings
from src.core.errors import BadRequestError
from src.core.events import run_debug_events
from src.core.logger import logger
from src.resources import strings

router = APIRouter()


@router.post("/{event_name}", tags=["debug"])
async def trigger_debug_task(event_name: str):
    """
    Manually trigger specific tasks for debugging.

    Args:
        event_name: The event to run ("currency", "shipping", "shipping_agg" or "all")
    """

    logger.info(strings.LOG_DEBUG_EVENT_START.format(event=event_name))

    if event_name not in settings.SERVICES_TYPES:
        raise BadRequestError(strings.ERR_INVALID_TASK)

    await run_debug_events(event_name)
    logger.info(strings.LOG_DEBUG_EVENT_COMPLETE.format(event=event_name))
    return Response(content=strings.LOG_DEBUG_EVENT_COMPLETE.format(event=event_name))
