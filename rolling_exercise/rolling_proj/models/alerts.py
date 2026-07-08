import uuid

from sqlalchemy import Column, ForeignKey, Date, Float
from sqlalchemy.dialects.postgresql import UUID

from database.connection import Base, engine


class Alerts(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True),
    date = Column(Date),
    aqi = Column(Float)
    # Only if we want to avoid dupelicating data
    # air_quality_id = Column(UUID(as_uuid=True), ForeignKey("air_quality.id"), nullable=False)


Base.metadata.create_all(engine)