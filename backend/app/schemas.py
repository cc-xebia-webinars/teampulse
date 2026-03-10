from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models import MoodType, TaskPriority, TaskStatus, TeamRole


class UserCreate(BaseModel):
    email: str
    password: str
    display_name: str
    avatar_url: str | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    display_name: str
    avatar_url: str | None
    created_at: datetime


class TeamCreate(BaseModel):
    name: str
    description: str


class TeamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    created_at: datetime


class TeamMembershipCreate(BaseModel):
    user_id: int
    team_id: int
    role: TeamRole = TeamRole.member


class TeamMembershipResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    team_id: int
    role: TeamRole
    joined_at: datetime


class StandupCreate(BaseModel):
    user_id: int
    team_id: int
    yesterday: str
    today: str
    blockers: str | None = None
    mood: MoodType


class StandupResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    team_id: int
    yesterday: str
    today: str
    blockers: str | None
    mood: MoodType
    created_at: datetime


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    assignee_id: int | None = None
    team_id: int
    created_by_id: int


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    assignee_id: int | None = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    assignee_id: int | None
    team_id: int
    created_by_id: int
    created_at: datetime
    updated_at: datetime
