from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import ValidationError
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.api.dependencies import get_parcel_type
from src.core.config import settings
from src.core.errors import NotFoundError
from src.core.logger import logger
from src.db.base import get_db
from src.db.models.parcels import Parcel, ParcelType
from src.resources import strings as s
from src.schemas.parcels import (
    ParcelCreate,
    ParcelCreateResponse,
    ParcelFilter,
    ParcelIdResponse,
    ParcelListResponse,
    ParcelTypesResponse,
)
from src.utils.utils import generate_uuid

router = APIRouter()


@router.post("/create", response_model=ParcelCreateResponse, tags=["parcels"])
async def create_parcel(
    parcel_entry: ParcelCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Registers a new parcel."""
    try:
        user_id = request.cookies.get(settings.SESSION_KEY, generate_uuid())
        parcel_type = await get_parcel_type(parcel_entry.type, db)

        new_parcel = Parcel(
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
            message=s.LOG_PARCEL_CREATED.format(id=new_parcel.id),
            parcel_id=new_parcel.id,
        )
    except Exception as e:
        logger.error(s.ERR_PARCEL_CREATE.format(error=str(e)))
        await db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=s.ERR_PARCEL_CREATE.format(error=str(e)),
        ) from e


@router.get("/types", response_model=List[ParcelTypesResponse], tags=["parcels"])
async def get_parcel_types(
    db: AsyncSession = Depends(get_db),
):
    """Retrieves all parcel types."""
    try:
        result = await db.execute(select(ParcelType))
        return result.scalars().all()
    except Exception as e:
        logger.error(s.ERR_PARCEL_TYPES.format(error=str(e)))
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=s.ERR_PARCEL_TYPES.format(error=str(e)),
        ) from e


@router.get("/list", response_model=ParcelListResponse, tags=["parcels"])
async def get_parcels_list(
    request: Request,
    parcel_filter: ParcelFilter = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Retrieves a list of parcels with pagination and filtering."""
    try:

        user_id = request.cookies.get(settings.SESSION_KEY, generate_uuid())

        query = select(Parcel).filter(Parcel.user_id == user_id)

        if parcel_filter.type is not None:
            query = query.filter(Parcel.type == parcel_filter.type)

        if parcel_filter.shipping_cost_calculated is not None:
            query = query.filter(
                Parcel.shipping_cost_rub.isnot(None)
                if parcel_filter.shipping_cost_calculated
                else Parcel.shipping_cost_rub.is_(None)
            )

        count_query = select(func.count()).select_from(query.subquery())
        total_count_result = await db.execute(count_query)
        total_count = total_count_result.scalar()

        paginated_query = query.offset(parcel_filter.offset).limit(parcel_filter.limit)
        parcels: List[Parcel] = (await db.execute(paginated_query)).scalars().all()

        for parcel in parcels:
            parcel.shipping_cost_rub = parcel.shipping_cost_rub_display

        return ParcelListResponse(
            total_count=total_count,
            parcels=parcels,
        )
    except Exception as e:
        logger.error(s.ERR_PARCEL_LIST.format(error=str(e)))
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=s.ERR_PARCEL_LIST.format(error=str(e)),
        ) from e


@router.get("/{parcel_id}", response_model=ParcelIdResponse, tags=["parcels"])
async def get_parcel(
    parcel_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Retrieves data for a specific parcel."""
    try:
        result = await db.execute(select(Parcel).filter(Parcel.id == parcel_id))
        parcel: Parcel = result.scalar_one_or_none()

        if not parcel:
            raise NotFoundError(s.ERR_PARCEL_NOT_FOUND.format(parcel_id=parcel_id))

        parcel.shipping_cost_rub = parcel.shipping_cost_rub_display

        return ParcelIdResponse(
            message=f"Parcel with ID={parcel_id!r} was successfully found.",
            **parcel.__dict__,
        )

    except NotFoundError as e:
        logger.warning(e.message)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=e.message) from e

    except Exception as e:
        logger.error(s.ERR_PARCEL_RETRIEVING.format(parcel_id=parcel_id, error=str(e)))
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=s.ERR_PARCEL_RETRIEVING.format(parcel_id=parcel_id, error=str(e)),
        ) from e
