import uvicorn
from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI

from db.session import get_db

app = FastAPI()
service_router = APIRouter()
events_router = APIRouter()


@service_router.get(path="/ping")
async def ping():
    return {"Success": True}


@events_router.get(path="/events")
async def get_events(db=Depends(get_db)):
    return {"Success": True}


app.include_router(service_router)
app.include_router(events_router)

if __name__ == "__main__":
    uvicorn.run(app)
