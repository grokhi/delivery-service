from pydantic import BaseModel, validator
from typing import Optional, List

class ParcelType(BaseModel):
    id: int
    name: str

class ParcelCreate(BaseModel):
    name: str
    weight: float
    type_id: int
    cost: float

    @validator('weight')
    def weight_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Weight must be a positive number")
        return value

    @validator('cost')
    def cost_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Cost must be a positive number")
        return value

class ParcelUpdate(BaseModel):
    name: Optional[str] = None
    weight: Optional[float] = None
    type_id: Optional[int] = None
    cost: Optional[float] = None

    @validator('weight', always=True)
    def weight_must_be_positive(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Weight must be a positive number")
        return value

    @validator('cost', always=True)
    def cost_must_be_positive(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Cost must be a positive number")
        return value

class Parcel(ParcelCreate):
    id: int
    shipping_cost: Optional[float] = None
    type: ParcelType

class ParcelFilter(BaseModel):
    user_id: int
    type: Optional[int] = None
    shipping_cost_calculated: Optional[bool] = None
    limit: int = 10
    offset: int = 0

class ParcelList(BaseModel):
    total_count: int
    parcels: List[Parcel]

class ParcelResponse(BaseModel):
    message: str
    parcel_id: Optional[int] = None
    parcel: Optional[Parcel] = None

class Currency(BaseModel):
    id: int
    rate: float

class CurrencyResponse(BaseModel):
    rate: float