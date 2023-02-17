import datetime
from typing import Generator

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from fastapi.params import Depends

from db.session import get_db

events_router = APIRouter()
api_v1_0_0_router = APIRouter()


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
):
    if start_date > end_date:
        raise HTTPException(
            status_code=422, detail="Start date can't be later, than end date"
        )
    return {"Success": True}


api_v1_0_0_router.include_router(events_router)
