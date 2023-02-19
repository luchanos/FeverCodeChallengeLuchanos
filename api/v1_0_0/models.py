import datetime
import uuid

from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class EventSummary(TunedModel):
    id: uuid.UUID
    title: str
    start_date: datetime.date
    start_time: datetime.time
    end_date: datetime.date
    end_time: datetime.time
    max_price: float
    min_price: float


class EventList(TunedModel):
    events: list[EventSummary]


class BaseResponse(TunedModel):
    data: EventList
