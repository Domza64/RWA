from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, BoardMembers
from app.models.board import Board


async def create_board(db: AsyncSession, name: str, description: str, user: User) -> int:
    result = await db.execute(
        insert(Board)
        .values(name=name, description=description)
        .returning(Board.board_id)
    )
    board_id = result.scalar_one()
    await db.execute(
        insert(BoardMembers)
        .values(board_id=board_id, user_id=user.user_id, role="ADMIN") # Kreator boarda je automatski admin
    )
    await db.flush()
    return board_id


async def get_boards_for_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Board)
        .join(BoardMembers)
        .where(BoardMembers.user_id == user_id)
    )
    return result.scalars().all()


async def user_has_access(db, user_id, board_id):
    result = await db.execute(
        select(BoardMembers).where(
            BoardMembers.user_id == user_id,
            BoardMembers.board_id == board_id
        )
    )
    return result.scalar_one_or_none() is not None


async def user_has_admin_access(db, user_id, board_id):
    result = await db.execute(
        select(BoardMembers).where(
            BoardMembers.user_id == user_id,
            BoardMembers.board_id == board_id
        )
    )
    user = result.scalar_one_or_none()
    return user is not None and user.role == "ADMIN"