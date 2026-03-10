from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Team, TeamMembership, User
from app.schemas import TeamCreate, TeamResponse

router = APIRouter(prefix="/api/teams", tags=["teams"])


class TeamMemberCreate(BaseModel):
    user_id: int


@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(payload: TeamCreate, db: Session = Depends(get_db)) -> Team:
    team = Team(**payload.model_dump())
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


@router.get("/", response_model=list[TeamResponse])
def list_teams(db: Session = Depends(get_db)) -> list[Team]:
    return db.query(Team).all()


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: int, db: Session = Depends(get_db)) -> Team:
    team = db.get(Team, team_id)
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team


@router.post("/{team_id}/members", response_model=TeamResponse)
def add_team_member(
    team_id: int, payload: TeamMemberCreate, db: Session = Depends(get_db)
) -> Team:
    team = db.get(Team, team_id)
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    user = db.get(User, payload.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    existing = (
        db.query(TeamMembership)
        .filter(TeamMembership.team_id == team_id, TeamMembership.user_id == payload.user_id)
        .first()
    )
    if existing is None:
        membership = TeamMembership(team_id=team_id, user_id=payload.user_id)
        db.add(membership)
        db.commit()

    db.refresh(team)
    return team
