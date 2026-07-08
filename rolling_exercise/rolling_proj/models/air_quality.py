import uuid
from sqlalchemy import Column, String, Date, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from database.connection import Base, engine
from pydantic import BaseModel, ConfigDict
from datetime import date

# Basic structure of air_quality table
class Air_Quality(Base):
    __tablename__ = "air_quality"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    date = Column(Date)
    city_name = Column(String)
    pm2_5 = Column(Integer)
    no2 = Column(Integer)
    co2 = Column(Integer)
    aqi = Column(Float)
    aqi_level = Column(String)


# Basic structure of air_quality table that is used in response
class Air_Quality_Response(BaseModel):
    id: uuid.UUID
    date: date
    city_name: str
    pm2_5: int
    no2: int
    co2: int
    aqi: float
    aqi_level: str

    model_config = ConfigDict(from_attributes=True)

Base.metadata.create_all(engine)