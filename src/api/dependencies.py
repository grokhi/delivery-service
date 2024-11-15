from __future__ import annotations

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import json
from redis import Redis
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.db.models import parcels
import httpx
import asyncio
import aioredis
from typing import Any, Dict, TYPE_CHECKING
import json

if TYPE_CHECKING:
    from .schemas.parcels import Parcel, ParcelType, ParcelCreate


# SQLALCHEMY_DATABASE_URL = os.getenv(
#     "DATABASE_URL", "mysql+mysqlconnector://root:@localhost/database"
# )

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def get_db():
#     """Gets a database session."""
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
