from fastapi import APIRouter

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html

# from src.redis import Redis
from sqlalchemy.orm import Session

from src.database import engine, SessionLocal, Base
from src.parcels.schemas import (
    ParcelCreate,
    Parcel,
    ParcelType,
    ParcelUpdate,
    ParcelFilter,
    ParcelList,
    ParcelResponse,
    Currency,
    CurrencyResponse,
)
from src.utils import get_db, get_redis, calculate_shipping_cost, get_exchange_rate

router = APIRouter()


@router.post("/parcel", response_model=ParcelResponse, tags=["Parcels"])
async def create_parcel(
    parcel: ParcelCreate, db: Session = Depends(get_db)  # , redis: Redis = Depends(get_redis)
):
    """Registers a new parcel."""
    try:
        new_parcel = Parcel(**parcel.dict())
        db.add(new_parcel)
        db.commit()
        db.refresh(new_parcel)
        return {"message": "Parcel registered successfully.", "parcel_id": new_parcel.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error registering parcel: {e}")


@router.get("/parcel-types", response_model=list[ParcelType], tags=["Parcels"])
async def get_parcel_types(db: Session = Depends(get_db)):
    """Retrieves all parcel types."""
    parcel_types = db.query(ParcelType).all()
    return parcel_types


@router.get("/parcels", response_model=ParcelList, tags=["Parcels"])
async def get_parcels(
    filter: ParcelFilter = Depends(),
    db: Session = Depends(get_db),
    # redis: Redis = Depends(get_redis),
):
    """Retrieves a list of parcels with pagination and filtering."""
    query = db.query(Parcel).filter(Parcel.user_id == filter.user_id)
    if filter.type:
        query = query.filter(Parcel.type_id == filter.type)
    if filter.shipping_cost_calculated:
        query = query.filter(Parcel.shipping_cost != None)  # Check for non-null values
    total_count = query.count()
    parcels = query.limit(filter.limit).offset(filter.offset).all()
    # for parcel in parcels:
    #     shipping_cost = redis.hget(f"parcel:{parcel.id}:shipping_cost", encoding="utf-8")
    #     if shipping_cost:
    #         parcel.shipping_cost = float(shipping_cost)
    #     else:
    #         parcel.shipping_cost = "Not calculated"
    return {"total_count": total_count, "parcels": parcels}


@router.get("/parcel/{parcel_id}", response_model=ParcelResponse, tags=["Parcels"])
async def get_parcel(
    parcel_id: int, db: Session = Depends(get_db)  # , redis: Redis = Depends(get_redis)
):
    """Retrieves data for a specific parcel."""
    parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")
    # shipping_cost = redis.hget(f"parcel:{parcel.id}:shipping_cost", encoding="utf-8")
    # if shipping_cost:
    #     parcel.shipping_cost = float(shipping_cost)
    # else:
    #     parcel.shipping_cost = "Not calculated"
    return parcel


@router.put("/parcel/{parcel_id}", response_model=ParcelResponse, tags=["Parcels"])
async def update_parcel(parcel_id: int, parcel: ParcelUpdate, db: Session = Depends(get_db)):
    """Updates an existing parcel."""
    db_parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not db_parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")
    db_parcel.name = parcel.name
    db_parcel.weight = parcel.weight
    db_parcel.type_id = parcel.type_id
    db_parcel.cost = parcel.cost
    db.commit()
    db.refresh(db_parcel)
    return db_parcel
