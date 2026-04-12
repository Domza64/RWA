from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.repositories import ticket_repo, board_repo
from app.schemas.ticket import TicketResponse, CreateTicketRequest


async def get_ticket(db: AsyncSession, user_id: int, ticket_id: int) -> TicketResponse:
    """Vraća ticket."""
    await check_access(db, user_id, ticket_id)

    ticket = await ticket_repo.get_ticket(db, ticket_id)
    if not ticket:
        raise AppError("not_found", "Ticket not found", 404)

    all_stages = await board_repo.get_workflow_stages(db, ticket.board_id)

    return TicketResponse(
        ticket_id=ticket.ticket_id,
        title=ticket.title,
        description=ticket.description,
        due_date=ticket.due_date,
        urgency=ticket.urgency,

        assignee=ticket.assignee,
        reporter=ticket.reporter,
        current_stage=ticket.current_stage,
        possible_stages=[stage for stage in all_stages],
    )


async def create_ticket(db: AsyncSession, board_id: int, user_id: int, body: CreateTicketRequest):
    has_access = await board_repo.user_has_access(db, user_id, board_id)
    if not has_access:
        raise AppError("forbidden", "You don't have access to this board", 403)

    ticket = await ticket_repo.add_ticket(db, board_id, body)
    t = ticket.scalar_one_or_none()
    print(t)
    return t




# ---- Helper funkcije ----

async def check_access(db: AsyncSession, user_id: int, ticket_id: int):
    has_access = True # TODO
    if not has_access:
        raise AppError("forbidden", "You don't have access to this ticket", 403)


async def check_admin_access(db: AsyncSession, user_id: int, ticket_id: int):
    has_access = True # TODO
    if not has_access:
        raise AppError("forbidden", "You don't have admin rights to this ticket", 403)
