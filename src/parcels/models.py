from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

Base = declarative_base()


class ParcelType(Base):
    __tablename__ = "parcel_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)

    parcels = relationship("Parcel", back_populates="parcel_type")


class Parcel(Base):
    __tablename__ = "parcels"  # Table name in the database

    id = Column(String(255), primary_key=True, index=True)
    user_id = Column(String(255))
    name = Column(String(255))
    weight = Column(Float)
    type_id = Column(Integer, ForeignKey("parcel_types.id"))  # Assuming there is a ParcelType model
    type = Column(String(255))  # Assuming there is a ParcelType model
    cost_usd = Column(Float)
    shipping_cost_rub = Column(Float)

    # Define relationship to ParcelType (optional if you want to access the type directly)
    parcel_type = relationship("ParcelType", back_populates="parcels")
