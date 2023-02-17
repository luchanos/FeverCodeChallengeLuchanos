import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI

from api.v1_0_0.handlers.event import api_v1_0_0_router

app = FastAPI()
service_router = APIRouter()


@service_router.get(path="/ping")
async def ping():
    return {"Success": True}


app.include_router(api_v1_0_0_router, prefix="/1.0.0", tags=["1.0.0"])

if __name__ == "__main__":
    uvicorn.run(app)
