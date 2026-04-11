from sqlalchemy import select, func
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import BoardMembers
from app.models.workflow_stage import WorkflowStage


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