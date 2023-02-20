import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI

from api.handlers.event import events_router

app = FastAPI()
service_router = APIRouter()


@service_router.get(path="/ping")
async def ping():
    return {"Success": True}


app.include_router(events_router)
app.include_router(service_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
