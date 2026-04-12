from sqlalchemy import insert, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, BoardMembers
from app.models.board import Board
from app.models.workflow_stage import WorkflowStage


async def create_board(db: AsyncSession, name: str, description: str, user: User) -> int:
    has_access = await db.execute(
        insert(Board)
        .values(name=name, description=description)
        .returning(Board.board_id)
    )
    board_id = has_access.scalar_one()
    await db.execute(
        insert(BoardMembers)
        .values(board_id=board_id, user_id=user.user_id, role="ADMIN") # Kreator boarda je automatski admin
    )
    await db.flush()
    return board_id


async def get_boards_for_user(db: AsyncSession, user_id: int):
    has_access = await db.execute(
        select(Board)
        .join(BoardMembers)
        .where(BoardMembers.user_id == user_id)
    )
    return has_access.scalars().all()


async def user_has_access(db, user_id, board_id) -> bool:
    has_access = await db.execute(
        select(BoardMembers).where(
            BoardMembers.user_id == user_id,
            BoardMembers.board_id == board_id
        )
    )
    return has_access.scalar_one_or_none() is not None


async def user_has_admin_access(db, user_id, board_id) -> bool:
    has_access = await db.execute(
        select(BoardMembers).where(
            BoardMembers.user_id == user_id,
            BoardMembers.board_id == board_id
        )
    )
    user = has_access.scalar_one_or_none()
    return user is not None and user.role == "ADMIN"


async def get_workflow_stages(db, board_id):
    has_access = await db.execute(
        select(WorkflowStage).where(
            WorkflowStage.board_id == board_id
        )
    )
    return has_access.scalars().all()


async def add_workflow_stage(db: AsyncSession, board_id: int, name: str):
    result = await db.execute(
        select(func.max(WorkflowStage.order))
        .where(WorkflowStage.board_id == board_id)
    )
    max_order = result.scalar_one()

    new_order = (max_order or 0) + 1

    await db.execute(
        insert(WorkflowStage).values(
            board_id=board_id,
            name=name,
            order=new_order
        )
    )
    await db.flush()