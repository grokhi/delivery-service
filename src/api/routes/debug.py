from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.api.dependencies import get_parcel_type
from src.core.config import settings
from src.core.events import run_debug_tasks

router = APIRouter()


@router.post("/{event_name}", tags=["debug"])
async def trigger_debug_task(event_name: str):
    """
    Manually trigger specific tasks for debugging.

    Args:
        event_name: The event to run ("currency", "shipping", or "all")
    """
    if event_name not in ["currency", "shipping", "all"]:
        raise HTTPException(
            status_code=400, detail="Invalid task name. Use 'currency', 'shipping', or 'all'"
        )

    await run_debug_tasks(event_name)
    return {"status": "success", "message": f"Debug task '{event_name}' completed"}
