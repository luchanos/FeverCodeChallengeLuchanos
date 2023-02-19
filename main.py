import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI

from api.v1_0_0.handlers.event import api_v1_0_0_router

# from starlette.requests import Request

app = FastAPI()
service_router = APIRouter()


# @app.middleware("http, https")
# async def response_middleware(request: Request, call_next):
#     response_result = {}
#     try:
#         return await call_next(request)
#         response_result["data"] = response
#     except Exception as err:
#         response_result["errors"] = err
#     return response_result


@service_router.get(path="/ping")
async def ping():
    return {"Success": True}


app.include_router(api_v1_0_0_router, prefix="/1.0.0", tags=["1.0.0"])

if __name__ == "__main__":
    uvicorn.run(app)
