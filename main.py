from fastapi import FastAPI, APIRouter
import uvicorn

app = FastAPI()
service_router = APIRouter()


def get_db():
    pass


@service_router.get(path="/ping")
def ping():
    return {"Success": True}


app.include_router(service_router)

if __name__ == "__main__":
    uvicorn.run(app)
