from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import BoardMembers


async def get_board_members(db: AsyncSession, board_id: int):
    result = await db.execute(
        select(BoardMembers)
        .options(selectinload(BoardMembers.user))
        .where(BoardMembers.board_id == board_id)
    )
    return result.scalars().all()


async def add_membership(db, board_id, user_id, role):
    await db.execute(
        insert(BoardMembers)
        .values(user_id=user_id, board_id=board_id, role=role)
    )
    await db.flush()
