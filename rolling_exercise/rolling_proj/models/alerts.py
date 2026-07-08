import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from database.connection import Base, engine


class Alerts(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    air_quality_id = Column(UUID(as_uuid=True), ForeignKey("air_quality.id"), nullable=False)


Base.metadata.create_all(engine)