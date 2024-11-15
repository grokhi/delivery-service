from __future__ import annotations

from fastapi import HTTPException
from src.db.models.parcels import Parcel, ParcelType

from typing import Any, Dict, TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_parcel_type(name: str, db: AsyncSession) -> ParcelType:
    # type_record = db.query(ParcelType).filter_by(name=name).first()
    result = await db.execute(select(ParcelType).filter_by(name=name))
    type_record = result.scalar()
    if not type_record:
        raise HTTPException(
            status_code=400, detail=f"Parcel type '{name}' not found in the database."
        )
    return type_record
