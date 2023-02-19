import datetime
import uuid

from pydantic import BaseModel


class EventResponse(BaseModel):
    id: uuid.UUID
    start_date: datetime.date
    start_time: datetime.time
    end_date: datetime.date
    end_time: datetime.time
    max_price: float
    min_price: float


class Data(BaseModel):
    events: list[EventResponse]


class BaseResponse(BaseModel):
    data: Data
