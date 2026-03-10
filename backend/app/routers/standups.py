from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Standup, Team, User
from app.schemas import StandupCreate, StandupResponse

router = APIRouter(prefix="/api/standups", tags=["standups"])


@router.post("/", response_model=StandupResponse, status_code=status.HTTP_201_CREATED)
def create_standup(payload: StandupCreate, db: Session = Depends(get_db)) -> Standup:
    user = db.get(User, payload.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    team = db.get(Team, payload.team_id)
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    standup = Standup(**payload.model_dump())
    db.add(standup)
    db.commit()
    db.refresh(standup)
    return standup


@router.get("/", response_model=list[StandupResponse])
def list_standups(team_id: int = Query(...), db: Session = Depends(get_db)) -> list[Standup]:
    standups = (
        db.query(Standup)
        .filter(Standup.team_id == team_id)
        .order_by(desc(Standup.created_at))
        .all()
    )
    return standups


@router.get("/today", response_model=list[StandupResponse])
def list_today_standups(
    team_id: int = Query(...), db: Session = Depends(get_db)
) -> list[Standup]:
    today = date.today()
    standups = (
        db.query(Standup)
        .filter(Standup.team_id == team_id)
        .filter(func.date(Standup.created_at) == today)
        .order_by(desc(Standup.created_at))
        .all()
    )
    return standups


@router.get("/{standup_id}", response_model=StandupResponse)
def get_standup(standup_id: int, db: Session = Depends(get_db)) -> Standup:
    standup = db.get(Standup, standup_id)
    if standup is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Standup not found")
    return standup
