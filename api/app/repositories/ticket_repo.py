from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket
from app.schemas.ticket import CreateTicketRequest


async def get_ticket(db: AsyncSession, ticket_id: int) -> Ticket | None:
    """Vraća ticket."""
    result = await db.execute(
        select(Ticket)
        .options(
            selectinload(Ticket.assignee),
            selectinload(Ticket.reporter),
            selectinload(Ticket.current_stage),
        )
        .where(Ticket.ticket_id == ticket_id)
    )
    return result.scalar_one_or_none()


async def add_ticket(
    db: AsyncSession,
    board_id: int,
    body: CreateTicketRequest
):
    ticket = await db.execute(
        insert(Ticket).values(
            title=body.title,
            description=body.description,
            due_date=body.due_date,
            urgency=body.urgency,
            board_id=board_id,
            assignee_id=body.asignee_id,
            reporter_id=body.reporter_id,
            stage_id=body.current_stage
        )
    )
    await db.flush()
    return ticket


async def get_board_tickets(db: AsyncSession, board_id: int):
    result = await db.execute(
        select(Ticket)
        .options(
            selectinload(Ticket.assignee),
            selectinload(Ticket.current_stage),
        )
        .where(Ticket.board_id == board_id)
    )
    return result.scalars().all()


async def get_assigned_tickets(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Ticket)
        .options(
            selectinload(Ticket.assignee),
            selectinload(Ticket.reporter),
            selectinload(Ticket.current_stage),
        )
        .where(Ticket.assignee_id == user_id)
    )
    return result.scalars().all()


async def get_reported_tickets(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Ticket)
        .options(
            selectinload(Ticket.assignee),
            selectinload(Ticket.reporter),
            selectinload(Ticket.current_stage),
        )
        .where(Ticket.reporter_id == user_id)
    )
    return result.scalars().all()