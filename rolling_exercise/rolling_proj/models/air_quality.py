import uuid

from sqlalchemy import Column, String, Date, Integer, Float
from sqlalchemy.dialects.postgresql import UUID

from database.connection import Base, engine


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


Base.metadata.create_all(engine)