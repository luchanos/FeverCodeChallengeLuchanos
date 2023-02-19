import datetime
from typing import Generator

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1_0_0.models import BaseResponse
from api.v1_0_0.models import Data
from api.v1_0_0.models import EventResponse
from db.dals import EventDAL
from db.session import get_db

events_router = APIRouter()
api_v1_0_0_router = APIRouter()


async def get_events_by_date_range(
    session: AsyncSession, start_date: datetime.datetime, end_date: datetime.datetime
) -> list[EventResponse]:
    async with session.begin():
        user_dal = EventDAL(session)
        events = await user_dal.get_events_by_time_range(
            start_date=start_date, end_date=end_date
        )
        result = []
        for event in events:
            event = dict(event)
            result.append(
                EventResponse(
                    **{
                        "id": event["id"],
                        "title": event["title"],
                        "start_date": event["event_start_date"].date(),
                        "start_time": event["event_start_date"].time(),
                        "end_date": event["event_end_date"].date(),
                        "end_time": event["event_end_date"].time(),
                        "max_price": event["max_price"],
                        "min_price": event["min_price"],
                    }
                )
            )
        return result


@events_router.get(path="/search")
async def get_events(
    start_date: datetime.datetime = Query(
        ...,
        description="Return only events that starts after this date",
        example="2017-07-21T17:32:28Z",
    ),
    end_date: datetime.datetime = Query(
        ...,
        description="Return only events that finishes before this date",
        example="2021-07-21T17:32:28Z",
    ),
    db: Generator = Depends(get_db),
) -> BaseResponse:
    if start_date > end_date:
        raise HTTPException(
            status_code=422, detail="Start date can't be later, than end date"
        )
    events = await get_events_by_date_range(
        session=db, start_date=start_date, end_date=end_date
    )
    return BaseResponse(data=Data(events=events))


api_v1_0_0_router.include_router(events_router)
