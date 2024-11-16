import uuid

from src.schemas.parcels import ParcelCreate


def calculate_shipping_cost(parcel: ParcelCreate, exchange_rate: float):
    """Calculates the shipping cost for a parcel."""
    return (parcel.weight * 0.5 + parcel.cost_usd * 0.01) * exchange_rate


def generate_uuid() -> str:
    return str(uuid.uuid4())
