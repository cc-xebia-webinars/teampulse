import logging

from fastapi import FastAPI

from app.middleware import logging_middleware
from app.routers import auth

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="TeamPulse API")

app.middleware("http")(logging_middleware)
app.include_router(auth.router)


@app.on_event("startup")
async def startup_message() -> None:
    print("TeamPulse API docs available at: http://localhost:8000/docs")
