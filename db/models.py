import uuid

from sqlalchemy import Column, String, Float, UniqueConstraint, Date, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Zone(Base):
    __tablename__ = "zones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(String)
    title = Column(String)
    zone_id = Column(String)
    price = Column(Float)
    start_date = Column(Date)
    start_time = Column(Time)
    end_date = Column(Date)
    end_time = Column(Time)

    UniqueConstraint("event_id", "zone_id", name="event_id_zone_id_idx")
