from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task, Team, User
from app.schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)) -> Task:
    team = db.get(Team, payload.team_id)
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    assignee_id = getattr(payload, "assignee_id", None)
    if assignee_id is not None and db.get(User, assignee_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignee user not found")

    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    team_id: int = Query(...),
    status_filter: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
) -> list[Task]:
    query = db.query(Task).filter(Task.team_id == team_id)
    if status_filter is not None:
        query = query.filter(Task.status == status_filter)
    return query.all()


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    changes = payload.model_dump(exclude_unset=True)
    assignee_id = changes.get("assignee_id")
    if assignee_id is not None and db.get(User, assignee_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignee user not found")

    for field_name, value in changes.items():
        setattr(task, field_name, value)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db.delete(task)
    db.commit()
    return None
