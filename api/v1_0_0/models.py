import datetime
import uuid

from pydantic import BaseModel
from pydantic import Field


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class EventSummary(TunedModel):
    id: uuid.UUID = Field(description="Identifier for the plan (UUID)")
    title: str = Field(description="Title of the plan")
    start_date: datetime.date = Field(
        description="Date when the event starts in local time"
    )
    start_time: datetime.time = Field(
        description="Time when the event starts in local time"
    )
    end_date: datetime.date = Field(
        description="Date when the event ends in local time"
    )
    end_time: datetime.time = Field(
        description="Time when the event ends in local time"
    )
    max_price: float = Field(description="Max price from all the available tickets")
    min_price: float = Field(description="Min price from all the available tickets")


class EventList(TunedModel):
    events: list[EventSummary] = Field(
        description="List of available events due to request parameters"
    )


class BaseResponse(TunedModel):
    data: EventList
