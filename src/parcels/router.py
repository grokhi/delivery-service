from fastapi import APIRouter

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html

# from src.redis import Redis
from sqlalchemy.orm import Session
import json
from src.parcels.schemas import (
    ParcelCreate,
    Parcel,
    ParcelIdResponse,
    ParcelFilter,
    ParcelListResponse,
    ParcelResponse,
    ParcelTypeResponse,
)
from src.utils import get_db, calculate_shipping_cost, get_exchange_rate
import uuid

router = APIRouter()
from fastapi import Cookie
from typing import *

from fastapi import FastAPI, Response
from sqlalchemy.exc import NoResultFound
from src.parcels import models
from src import utils, strings
from src.tasks import get_redis
from aioredis import Redis


@router.post("/create", response_model=ParcelResponse, tags=["parcels"])
async def create_parcel(
    parcel_entry: ParcelCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """Registers a new parcel."""
    try:
        user_id = request.cookies.get(strings.SESSION_KEY, utils.generate_uuid())
        parcel_id = f"{user_id}__{utils.generate_uuid()}"

        parcel_type = utils.get_parcel_type(parcel_entry.type, db)

        new_parcel = models.Parcel(
            id=parcel_id,
            user_id=user_id,
            name=parcel_entry.name,
            weight=parcel_entry.weight,
            type_id=parcel_type.id,
            type=parcel_type.name,
            cost_usd=parcel_entry.cost_usd,
        )
        db.add(new_parcel)
        db.commit()
        db.refresh(new_parcel)
        return ParcelResponse(
            message="Parcel registered successfully.",
            parcel_id=new_parcel.id,
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error registering parcel: {e}")


@router.get("/types", response_model=list[ParcelTypeResponse], tags=["parcels"])
async def get_parcel_types(db: Session = Depends(get_db)):
    """Retrieves all parcel types."""
    parcel_types = db.query(models.ParcelType).all()
    return parcel_types


@router.get("/list", response_model=ParcelListResponse, tags=["parcels"])
async def get_parcels_list(
    request: Request,
    parcel_filter: ParcelFilter = Depends(),
    db: Session = Depends(get_db),
):
    """Retrieves a list of parcels with pagination and filtering."""
    user_id = request.cookies.get(strings.SESSION_KEY, utils.generate_uuid())
    parcels = db.query(models.Parcel).filter(models.Parcel.user_id == user_id)
    if parcel_filter.type:
        parcels = parcels.filter(models.Parcel.type == parcel_filter.type)

    # if parcel_filter.shipping_cost_calculated:
    #     parcels = parcels.filter(
    #         models.Parcel.shipping_cost_rub != None
    #     )  # Check for non-null values

    total_count = parcels.count()
    parcels = parcels.limit(parcel_filter.limit).offset(parcel_filter.offset).all()

    # for parcel in parcels:
    #     shipping_cost = redis.hget(f"parcel:{parcel.id}:shipping_cost", encoding="utf-8")
    #     if shipping_cost:
    #         parcel.shipping_cost = float(shipping_cost)
    #     else:
    #         parcel.shipping_cost = "Not calculated"

    return ParcelListResponse(
        total_count=total_count, parcels=[Parcel.from_orm(parcel) for parcel in parcels]
    )


@router.get("/{parcel_id}", response_model=ParcelIdResponse, tags=["parcels"])
async def get_parcel(
    parcel_id: str,
    db: Session = Depends(get_db),  # , redis: Redis = Depends(get_redis)
):
    """Retrieves data for a specific parcel."""
    parcel = db.query(models.Parcel).filter(models.Parcel.id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")
    # shipping_cost = redis.hget(f"parcel:{parcel.id}:shipping_cost", encoding="utf-8")
    # if shipping_cost:
    #     parcel.shipping_cost = float(shipping_cost)
    # else:
    #     parcel.shipping_cost = "Not calculated"
    return ParcelIdResponse(
        message=f"Parcel with ID={parcel_id!r} was successfully found.", **parcel.__dict__
    )
