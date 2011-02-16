import uuid

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    base_event_id = Column(String)
    title = Column(String)
    price = Column(Float)
    event_start_date = Column(DateTime(timezone=True))
    event_end_date = Column(DateTime(timezone=True))
    zone_id = Column(String)
    __table_args__ = (
        UniqueConstraint(
            "base_event_id", "zone_id", "price", name="base_event_id_zone_id_price_idx"
        ),
    )
