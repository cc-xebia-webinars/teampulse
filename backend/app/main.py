import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middleware import logging_middleware
from app.routers import auth
from app.database import Base, engine
from app.routers.standups import router as standups_router
from app.routers.tasks import router as tasks_router
from app.routers.teams import router as teams_router
from app.routers.users import router as users_router


logging.basicConfig(level=logging.INFO)

app = FastAPI(title="TeamPulse API")

app.middleware("http")(logging_middleware)
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_message() -> None:
    print("TeamPulse API docs available at: http://localhost:8000/docs")

@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "app": "TeamPulse"}


app.include_router(users_router)
app.include_router(teams_router)
app.include_router(standups_router)
app.include_router(tasks_router)
