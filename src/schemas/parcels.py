from __future__ import annotations

from pydantic import BaseModel, field_validator, Field
from typing import Optional, List, Literal, Union
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from src.resources import strings
from src.db.models import parcels
from src.db.base import get_db
from src.core.config import settings


class ParcelCreate(BaseModel):
    name: str = Field(default="some_parcel")
    weight: float = Field(default=1.0)
    type: str = Field(default=settings.PARCEL_TYPES[0])
    cost_usd: float = Field(default=1.0)

    @field_validator("weight")
    @classmethod
    def weight_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Weight must be a positive number")
        return value

    @field_validator("type")
    @classmethod
    def category_must_be_allowed(cls, value):
        if value not in settings.PARCEL_TYPES:
            raise ValueError(
                f"Type {value!r} is not allowed. Allowed types: {settings.PARCEL_TYPES}"
            )
        return value

    @field_validator("cost_usd")
    @classmethod
    def cost_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Cost must be a positive number")
        return value


class Parcel(ParcelCreate):
    id: int
    user_id: str
    type_id: int
    type: str
    shipping_cost_rub: Optional[Union[float, str]] = None

    class Config:
        # orm_mode = True
        from_attributes = True


class ParcelFilter(BaseModel):
    type: Optional[str] = None
    shipping_cost_calculated: bool = True
    limit: int = 10
    offset: int = 0


class ParcelListResponse(BaseModel):
    total_count: int
    parcels: List[Parcel]

    class Config:
        # orm_mode = True
        from_attributes = True


class ParcelCreateResponse(BaseModel):
    message: str
    parcel_id: Optional[int] = None


class ParcelTypesResponse(BaseModel):
    id: int
    name: str

    class Config:
        # orm_mode = True
        from_attributes = True


class ParcelIdResponse(BaseModel):
    weight: float
    type: str
    cost_usd: float
    shipping_cost_rub: Union[float, str]

    class Config:
        # orm_mode = True
        from_attributes = True
