from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, BoardMembers
from app.models.board import Board


async def create_board(db: AsyncSession, name: str, description: str, user: User) -> int:
    """Create a new board."""
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
    """Get all boards belonging to a user."""
    result = await db.execute(
        select(Board)
        .join(BoardMembers)
        .where(BoardMembers.user_id == user_id)
    )
    return result.scalars().all()