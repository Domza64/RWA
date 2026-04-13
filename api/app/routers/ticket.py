from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import deps
from app.core.deps import get_db
from app.models import User
from app.schemas.ticket import TicketResponse
from app.services import ticket_service

router = APIRouter()


@router.get("/assigned", response_model=List[TicketResponse])
async def get_assigned_tickets(db: AsyncSession = Depends(get_db), user: User = Depends(deps.get_current_user)):
    """Vraća assigned tickete."""
    return await ticket_service.get_tickets(db, user.user_id, "ASSIGNED")


@router.get("/reported", response_model=List[TicketResponse])
async def get_reported_tickets(db: AsyncSession = Depends(get_db), user: User = Depends(deps.get_current_user)):
    """Vraća reported tickete."""
    return await ticket_service.get_tickets(db, user.user_id, "REPORTED")


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(deps.get_current_user)):
    """Vraća ticket."""
    ticket = await ticket_service.get_ticket(db, user.user_id, ticket_id)
    return ticket