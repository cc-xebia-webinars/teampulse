import hashlib
from datetime import datetime, timedelta, timezone

from app.database import Base, SessionLocal, engine
from app.models import MoodType, Standup, Task, TaskPriority, TaskStatus, Team, TeamMembership, TeamRole, User


def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def seed() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        db.query(Task).delete()
        db.query(Standup).delete()
        db.query(TeamMembership).delete()
        db.query(Team).delete()
        db.query(User).delete()
        db.commit()

        password_hash = get_password_hash("password123")

        users = [
            User(email="alice@teampulse.dev", hashed_password=password_hash, display_name="Alice"),
            User(email="bob@teampulse.dev", hashed_password=password_hash, display_name="Bob"),
            User(email="carol@teampulse.dev", hashed_password=password_hash, display_name="Carol"),
            User(email="dave@teampulse.dev", hashed_password=password_hash, display_name="Dave"),
        ]
        db.add_all(users)
        db.flush()

        engineering = Team(name="Engineering", description="Core product engineering team")
        db.add(engineering)
        db.flush()

        memberships = [
            TeamMembership(user_id=users[0].id, team_id=engineering.id, role=TeamRole.admin),
            TeamMembership(user_id=users[1].id, team_id=engineering.id, role=TeamRole.member),
            TeamMembership(user_id=users[2].id, team_id=engineering.id, role=TeamRole.member),
            TeamMembership(user_id=users[3].id, team_id=engineering.id, role=TeamRole.member),
        ]
        db.add_all(memberships)

        now = datetime.now(timezone.utc)
        standups = [
            Standup(
                user_id=users[0].id,
                team_id=engineering.id,
                yesterday="Implemented JWT auth endpoints.",
                today="Start integrating auth in frontend.",
                blockers=None,
                mood=MoodType.great,
                created_at=now - timedelta(days=2, hours=1),
            ),
            Standup(
                user_id=users[1].id,
                team_id=engineering.id,
                yesterday="Refactored task card component.",
                today="Add drag-and-drop polish.",
                blockers="Need UX copy finalization.",
                mood=MoodType.good,
                created_at=now - timedelta(days=2, minutes=30),
            ),
            Standup(
                user_id=users[2].id,
                team_id=engineering.id,
                yesterday="Wrote initial API tests.",
                today="Increase test coverage for tasks.",
                blockers=None,
                mood=MoodType.okay,
                created_at=now - timedelta(days=1, hours=2),
            ),
            Standup(
                user_id=users[3].id,
                team_id=engineering.id,
                yesterday="Debugged CI failures.",
                today="Stabilize deployment pipeline.",
                blockers="Intermittent flaky tests.",
                mood=MoodType.struggling,
                created_at=now - timedelta(days=1, minutes=45),
            ),
            Standup(
                user_id=users[0].id,
                team_id=engineering.id,
                yesterday="Completed auth integration in UI.",
                today="Review pending PRs.",
                blockers=None,
                mood=MoodType.good,
                created_at=now - timedelta(hours=3),
            ),
        ]
        db.add_all(standups)

        tasks = [
            Task(
                title="Build login API",
                description="Implement token-based authentication endpoint.",
                status=TaskStatus.done,
                priority=TaskPriority.high,
                assignee_id=users[0].id,
                team_id=engineering.id,
                created_by_id=users[0].id,
            ),
            Task(
                title="Create standup form UI",
                description="Frontend form for yesterday/today/blockers/mood.",
                status=TaskStatus.in_progress,
                priority=TaskPriority.high,
                assignee_id=users[1].id,
                team_id=engineering.id,
                created_by_id=users[0].id,
            ),
            Task(
                title="Task board drag-and-drop",
                description="Enable reordering and status moves.",
                status=TaskStatus.todo,
                priority=TaskPriority.medium,
                assignee_id=users[1].id,
                team_id=engineering.id,
                created_by_id=users[2].id,
            ),
            Task(
                title="Write API integration tests",
                description="Cover users, teams, standups, and tasks endpoints.",
                status=TaskStatus.in_progress,
                priority=TaskPriority.high,
                assignee_id=users[2].id,
                team_id=engineering.id,
                created_by_id=users[3].id,
            ),
            Task(
                title="Set up CI lint checks",
                description=None,
                status=TaskStatus.done,
                priority=TaskPriority.medium,
                assignee_id=users[3].id,
                team_id=engineering.id,
                created_by_id=users[3].id,
            ),
            Task(
                title="Prepare sprint demo",
                description="Summarize completed stories and blockers.",
                status=TaskStatus.todo,
                priority=TaskPriority.low,
                assignee_id=None,
                team_id=engineering.id,
                created_by_id=users[0].id,
            ),
        ]
        db.add_all(tasks)
        db.commit()

    print("Seed complete: 4 users, 1 team, 5 standups, 6 tasks.")


if __name__ == "__main__":
    seed()
