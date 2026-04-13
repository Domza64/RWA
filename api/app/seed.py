# =============================================================
# seed.py — Inicijalni podaci za razvoj i testiranje
# =============================================================
# Kreira nekakve ostnovne podatke za testiranje
#
# Pokretanje (iz api/ direktorija):
#   python -m app.seed
#
# Zašto seed?
#   - Nakon "alembic upgrade head" imamo prazne tablice
#   - Za razvoj trebamo barem admin login i klubove
#   - Za testiranje auth/ownership logike (predavanje 3-4)
#     trebamo dva kluba da dokažemo da jedan ne vidi drugog
#
# Idempotentnost:
#   Skripta provjerava postoji li već zapis s istim username/imenom.
#   Ako postoji — preskače. Sigurno je pokrenuti višestruko.
# =============================================================

import asyncio
import logging

import bcrypt as _bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.board_members import BoardMembers
from app.models.workflow_stage import WorkflowStage
from app.models.board import Board

from app.core.database import AsyncSessionLocal, engine
from app.models.ticket import Ticket
from app.models.user import User

from datetime import datetime, timedelta

now = datetime.utcnow()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---- Seed podaci ------------------------------------------------

USERS = [
    {
        "username": "user1",
        "email": "user1@mail.com",
        "password": "password1"
    },
    {
        "username": "user2",
        "email": "user2@mail.com",
        "password": "password1"
    },
    {
        "username": "user3",
        "email": "user3@mail.com",
        "password": "password1"
    }
]

BOARDS = [
    {
        "name": "Unizd board",
        "description": "Bord s taskovima za unizd",
    },
    {
        "name": "Neki board",
        "description": "Vrlo kreativan board",
    },
    {
        "name": "Vazni zadatci",
        "description": "Tu je nesto sto hitno treba biti napravljeno",
    }
]

WORKFLOW_STAGES = [
    {
        "stage_id": 1,
        "name": "TODO",
        "order": 1,
        "board_id": 1
    },
    {
        "stage_id": 2,
        "name": "IN PROGRESS",
        "order": 2,
        "board_id": 1
    },
    {
        "stage_id": 3,
        "name": "COMPLETED",
        "order": 3,
        "board_id": 1
    },
    {
        "stage_id": 4,
        "name": "TODO",
        "order": 1,
        "board_id": 2
    }
]

BOARD_MEMBERS = [
    {
        "user_id": 1,
        "board_id": 1,
        "role": "ADMIN"
    },
    {
        "user_id": 2,
        "board_id": 2,
        "role": "ADMIN"
    },
    {
        "user_id": 3,
        "board_id": 3,
        "role": "ADMIN"
    },
    {
        "user_id": 1,
        "board_id": 2,
        "role": "MEMBER"
    }
]

TICKETS = [
    {
        "title": "Implement login",
        "description": "JWT login + refresh tokens",
        "due_date": now + timedelta(days=3),
        "urgency": 3,
        "assignee_id": 1,
        "reporter_id": 2,
        "board_id": 1,
        "stage_id": 1
    },
    {
        "title": "Fix bug #42",
        "description": "Crash when creating ticket",
        "due_date": None,
        "urgency": 5,
        "assignee_id": 1,
        "reporter_id": 1,
        "board_id": 1,
        "stage_id": 2
    },
    {
        "title": "Design landing page",
        "description": "Create Figma mockups",
        "due_date": now + timedelta(days=5),
        "urgency": 2,
        "assignee_id": 1,
        "reporter_id": 1,
        "board_id": 2,
        "stage_id": 4
    },
    {
        "title": "Database optimization",
        "description": "Add indexes and improve queries",
        "due_date": now + timedelta(days=7),
        "urgency": 4,
        "assignee_id": 1,
        "reporter_id": 3,
        "board_id": 3,
        "stage_id": None
    },
    {
        "title": "Write unit tests",
        "description": "Coverage at least 80%",
        "due_date": now + timedelta(days=4),
        "urgency": 3,
        "assignee_id": 2,
        "reporter_id": 1,
        "board_id": 3,
        "stage_id": None
    }
]

def _hash_pw(plain: str) -> str:
    return _bcrypt.hashpw(plain.encode(), _bcrypt.gensalt()).decode()


async def seed_users(session: AsyncSession):
    for data in USERS:
        result = await session.execute(
            select(User).where(User.username == data["username"])
        )
        if result.scalar_one_or_none():
            continue

        user = User(
            username=data["username"],
            email=data["email"],
            password_hash=_hash_pw(data["password"]),
        )
        session.add(user)
        logger.info("User created: %s", user.username)

    await session.commit()


async def seed_boards(session: AsyncSession):
    for data in BOARDS:
        result = await session.execute(
            select(Board).where(Board.name == data["name"])
        )
        if result.scalar_one_or_none():
            continue

        board = Board(**data)
        session.add(board)
        logger.info("Board created: %s", board.name)

    await session.commit()


async def seed_stages(session: AsyncSession):
    for data in WORKFLOW_STAGES:
        result = await session.execute(
            select(WorkflowStage).where(
                WorkflowStage.name == data["name"],
                WorkflowStage.board_id == data["board_id"]
            )
        )
        if result.scalar_one_or_none():
            continue

        stage = WorkflowStage(**data)
        session.add(stage)

    await session.commit()


async def seed_board_members(session: AsyncSession):
    for data in BOARD_MEMBERS:
        result = await session.execute(
            select(BoardMembers).where(
                BoardMembers.user_id == data["user_id"],
                BoardMembers.board_id == data["board_id"]
            )
        )
        if result.scalar_one_or_none():
            continue

        member = BoardMembers(**data)
        session.add(member)

    await session.commit()


async def seed_tickets(session: AsyncSession):
    for data in TICKETS:
        result = await session.execute(
            select(Ticket).where(Ticket.title == data["title"])
        )
        if result.scalar_one_or_none():
            continue

        ticket = Ticket(**data)
        session.add(ticket)

    await session.commit()


async def seed(session: AsyncSession) -> None:
    await seed_users(session)
    await seed_boards(session)
    await seed_stages(session)
    await seed_board_members(session)
    await seed_tickets(session)

    await session.commit()
    logger.info("Seed completed successfully!")


async def main() -> None:
    """Entry point — otvara sesiju, pokreće seed, zatvara engine."""
    async with AsyncSessionLocal() as session:
        await seed(session)
    # Čisto zatvaranje svih konekcija u poolu.
    await engine.dispose()


# Omogućuje pokretanje sa: python -m app.seed
if __name__ == "__main__":
    asyncio.run(main())
