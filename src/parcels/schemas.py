from __future__ import annotations

from pydantic import BaseModel, validator, Field
from typing import Optional, List, Literal
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from src import strings
from src.parcels import models
from src.utils import get_db


def get_allowed_types():
    db = next(get_db())
    return [name[0] for name in db.query(models.ParcelType.name).all()]


class ParcelCreate(BaseModel):
    name: str = Field(default="some_parcel")
    weight: float = Field(default=1.0)
    type: str = Field(default="other")
    cost_usd: float = Field(default=1.0)

    @validator("weight")
    def weight_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Weight must be a positive number")
        return value

    @validator("type")
    def category_must_be_allowed(cls, value):
        allowed = get_allowed_types()
        if value not in allowed:
            raise ValueError(f"Type {value!r} is not allowed. Allowed types: {allowed}")
        return value

    @validator("cost_usd")
    def cost_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Cost must be a positive number")
        return value


class Parcel(ParcelCreate):
    id: str
    user_id: str
    type_id: int
    type: str
    shipping_cost_rub: Optional[float] = None

    class Config:
        orm_mode = True


class ParcelFilter(BaseModel):
    type: Optional[str] = Field(default="other")
    shipping_cost_calculated: Optional[bool] = None
    limit: int = 10
    offset: int = 0


class ParcelListResponse(BaseModel):
    total_count: int
    parcels: List[Parcel]

    class Config:
        orm_mode = True


class ParcelResponse(BaseModel):
    message: str
    parcel_id: Optional[str] = None


class ParcelTypeResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ParcelIdResponse(BaseModel):
    weight: float
    type: str
    cost_usd: float
    shipping_cost_rub: float

    class Config:
        orm_mode = True
