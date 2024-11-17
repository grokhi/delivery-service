from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ParcelType(Base):
    __tablename__ = "parcel_types"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    parcels = relationship("Parcel", back_populates="parcel_type")
    shipping_aggregates = relationship("ShippingCostRubAgg", back_populates="parcel_type")


class Parcel(Base):
    __tablename__ = "parcels"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(255))
    name = Column(String(255))
    weight = Column(Float)
    type_id = Column(Integer, ForeignKey("parcel_types.id"))
    type = Column(String(255))
    cost_usd = Column(Float)
    shipping_cost_rub = Column(Float)

    parcel_type = relationship("ParcelType", back_populates="parcels")

    @property
    def shipping_cost_rub_display(self):
        return (
            self.shipping_cost_rub if self.shipping_cost_rub is not None else "Not calculated yet."
        )


class ShippingCostRubAgg(Base):
    __tablename__ = "shipping_cost_rub_agg"

    id = Column(String(255), primary_key=True)
    timestamp = Column(DateTime)
    type_id = Column(Integer, ForeignKey("parcel_types.id"), nullable=False)
    type = Column(String(255), nullable=False)
    shipping_cost_rub = Column(Float, nullable=False)

    parcel_type = relationship("ParcelType", back_populates="shipping_aggregates")
