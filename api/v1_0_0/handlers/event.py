from fastapi import APIRouter
from fastapi.params import Depends

from db.session import get_db

events_router = APIRouter()
api_v1_0_0_router = APIRouter()


@events_router.get(path="/search")
async def get_events(db=Depends(get_db)):
    return {"Success": True}


api_v1_0_0_router.include_router(events_router)
