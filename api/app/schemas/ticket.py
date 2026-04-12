from datetime import date
from typing import List, Literal

from pydantic import BaseModel, Field

from app.schemas.auth import UserResponse


class WorkflowStageDTO(BaseModel):
    stage_id: int
    stage_name: str


class TicketResponse(BaseModel):
    """Odgovor s podatcima o ticketu"""
    ticket_id: int
    title: str
    description: str
    due_date: date | None
    urgency: int

    assignee: UserResponse | None
    reporter: UserResponse
    current_stage: WorkflowStageDTO | None
    possible_stages: List[WorkflowStageDTO]


class CreateTicketRequest(BaseModel):
    """Tijelo POST /{board_id}/ticket requesta."""
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=400)
    due_date: date | None = None # TODO: validate
    urgency: Literal[1, 2, 3, 4, 5]
    asignee_id: int | None = None
    reporter_id: int
    current_stage: int | None = None