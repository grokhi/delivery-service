from fastapi import APIRouter

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html

# from src.redis import Redis
from sqlalchemy.orm import Session
from sqlalchemy import func
import json
from src.resources import strings
from src.schemas.parcels import (
    ParcelCreate,
    Parcel,
    ParcelIdResponse,
    ParcelFilter,
    ParcelListResponse,
    ParcelCreateResponse,
    ParcelTypesResponse,
)
from src.utils.utils import (
    calculate_shipping_cost,
    get_exchange_rate,
    generate_uuid,
    get_parcel_type,
)
from src.db.base import get_db
import uuid
from src.db.models.parcels import Parcel, ParcelType

router = APIRouter()
from fastapi import Cookie
from typing import *

from fastapi import FastAPI, Response
from sqlalchemy.exc import NoResultFound

from src import utils
from src.core.cache import get_redis
from src.core.config import settings
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


@router.post("/create", response_model=ParcelCreateResponse, tags=["parcels"])
async def create_parcel(
    parcel_entry: ParcelCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Registers a new parcel."""
    try:
        user_id = request.cookies.get(settings.SESSION_KEY, generate_uuid())
        parcel_id = f"{user_id}__{generate_uuid()}"

        parcel_type = await get_parcel_type(parcel_entry.type, db)

        new_parcel = Parcel(
            id=parcel_id,
            user_id=user_id,
            name=parcel_entry.name,
            weight=parcel_entry.weight,
            type_id=parcel_type.id,
            type=parcel_type.name,
            cost_usd=parcel_entry.cost_usd,
        )
        db.add(new_parcel)
        await db.commit()
        await db.refresh(new_parcel)
        return ParcelCreateResponse(
            message="Parcel registered successfully.",
            parcel_id=new_parcel.id,
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error registering parcel: {e}")


@router.get("/types", response_model=List[ParcelTypesResponse], tags=["parcels"])
async def get_parcel_types(
    db: AsyncSession = Depends(get_db),
):
    """Retrieves all parcel types."""
    result = await db.execute(select(ParcelType))
    return result.scalars().all()


# def _format_parcel_response(parcel):
#     parcel_data = Parcel.from_orm(parcel)
#     parcel_data.shipping_cost_rub = parcel_data.shipping_cost_rub_display
#     return parcel_data


@router.get("/list", response_model=ParcelListResponse, tags=["parcels"])
async def get_parcels_list(
    request: Request,
    parcel_filter: ParcelFilter = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Retrieves a list of parcels with pagination and filtering."""
    user_id = request.cookies.get(strings.SESSION_KEY, generate_uuid())

    query = select(Parcel).filter(Parcel.user_id == user_id)

    if parcel_filter.type is not None:
        query = query.filter(Parcel.type == parcel_filter.type)

    if parcel_filter.shipping_cost_calculated is not None:
        query = query.filter(Parcel.shipping_cost_rub.is_(parcel_filter.shipping_cost_calculated))

    total_count = await db.execute(select(func.count()).select_from(query.subquery()))
    query = query.offset(parcel_filter.offset).limit(parcel_filter.limit)
    parcels = (await db.execute(query)).scalars().all()

    return ParcelListResponse(total_count=total_count, parcels=parcels)


@router.get("/{parcel_id}", response_model=ParcelIdResponse, tags=["parcels"])
async def get_parcel(
    parcel_id: str,
    db: AsyncSession = Depends(get_db),  # , redis: Redis = Depends(get_redis)
):
    """Retrieves data for a specific parcel."""
    result = await db.execute(select(Parcel).filter(Parcel.id == parcel_id))
    parcel = result.scalar_one_or_none()

    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")

    return ParcelIdResponse(
        message=f"Parcel with ID={parcel_id!r} was successfully found.",
        **parcel.__dict__,
    )
