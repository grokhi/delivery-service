from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import json
from redis import Redis

from .parcels.schemas import Parcel, ParcelType, Currency

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./delivery.db")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Gets a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis():
    """Gets a Redis connection."""
    redis = Redis(host="redis", port=6379)
    return redis


def calculate_shipping_cost(parcel: Parcel, exchange_rate: float):
    """Calculates the shipping cost for a parcel."""
    return (parcel.weight * 0.5 + parcel.cost * 0.01) * exchange_rate


def get_exchange_rate(redis: Redis):
    """Retrieves the exchange rate from Redis."""
    exchange_rate = redis.get("exchange_rate", encoding="utf-8")
    if exchange_rate:
        return float(exchange_rate)
    else:
        # Load from file if not in cache
        with open("currencies_json.js", "r") as f:
            exchange_rate_data = json.load(f)
            exchange_rate = exchange_rate_data["RUB"]
            redis.set("exchange_rate", exchange_rate)
        return exchange_rate
