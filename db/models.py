import datetime
import uuid

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseEvent(Base):
    __tablename__ = "base_events"

    base_event_id = Column(String, primary_key=True)
    sell_mode = Column(String)
    title = Column(String)
    is_active = Column(Boolean, default=True)
    last_updated_dt = Column(DateTime(timezone=True), default=datetime.datetime.now())


class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_start_date = Column(DateTime(timezone=True))
    event_end_date = Column(DateTime(timezone=True))
    event_id = Column(String)
    base_event_id = Column(String, ForeignKey("base_events.base_event_id"))
    is_active = Column(Boolean, default=True)
    zones = Column(JSONB)
    last_updated_dt = Column(DateTime(timezone=True), default=datetime.datetime.now())

    __table_args__ = (
        UniqueConstraint(
            "base_event_id", "event_id", name="base_event_id_event_id_idx"
        ),
    )
