import uuid

from pydantic import ConfigDict
from sqlalchemy import Column, Date, Float
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel, ConfigDict
from datetime import date
from database.connection import Base, engine

# Basic structure of alerts table 
class Alerts(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    date = Column(Date)
    aqi = Column(Float)
    # Only if we want to avoid dupelicating data
    # air_quality_id = Column(UUID(as_uuid=True), ForeignKey("air_quality.id"), nullable=False)

# Basic structure of alerts table that is used in response
class Alerts_Response(BaseModel):
    id: uuid.UUID
    date: date
    city_name: str

    model_config = ConfigDict(from_attributes=True)

Base.metadata.create_all(engine)