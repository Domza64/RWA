from typing import List

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.core import deps
from app.core.deps import get_db
from app.models import User
from app.schemas.board import CreateBoardRequest, CreateBoardResponse, AddUserRequest, \
    BoardUserResponse, AddWorkflowStageRequest, WorkflowStageResponse
from app.schemas.ticket import CreateTicketRequest
from app.services import board_service, ticket_service
from app.schemas.board import BoardDTO

router = APIRouter()


@router.get("", response_model=list[BoardDTO])
async def get_boards(db: AsyncSession = Depends(get_db), user: User = Depends(deps.get_current_user)):
    """Vraća listu boardova korisnika."""
    return await board_service.get_boards(db, user.user_id)


@router.post("", response_model=CreateBoardResponse)
async def create_board(body: CreateBoardRequest, db: AsyncSession = Depends(get_db), user: User = Depends(deps.get_current_user)):
    """Kreira novi board"""
    board_id = await board_service.create_board(db, user, body.name, body.description)
    return CreateBoardResponse(board_id=board_id)


@router.get("/{board_id}", response_model=BoardDTO)
async def get_board(board_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(deps.get_current_user)):
    """Vraća board info."""
    board = await board_service.get_board(db, board_id, user.user_id)
    if not board:
        raise AppError("not_found", "Board not found", 404)
    return board


@router.get("/{board_id}/members", response_model=List[BoardUserResponse])
async def get_members(board_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(deps.get_current_user)):
    """Vraća listu članova boardova."""
    members = await board_service.get_members(db, board_id, user.user_id)
    return members


@router.post("/{board_id}/members")
async def add_member(body: AddUserRequest, board_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(deps.get_current_user)):
    """Dodaje novog člana na board"""
    await board_service.add_member(db, board_id, user, body.user_id, body.role)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post("/{board_id}/workflow-stage")
async def add_workflow_stage(body: AddWorkflowStageRequest, board_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(deps.get_current_user)):
    """Dodaje novi ticket status na board"""
    await board_service.add_workflow_stage(db, board_id, user, body.name)
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/{board_id}/workflow-stages", response_model=List[WorkflowStageResponse])
async def get_workflow_stages(board_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(deps.get_current_user)):
    """Vraća listu workflow stageva na boardu"""
    stages = await board_service.get_workflow_stages(db, board_id, user.user_id)
    return [workflow_stage for workflow_stage in stages]


@router.post("/{board_id}/ticket")
async def create_ticket(body: CreateTicketRequest, board_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(deps.get_current_user)):
    await ticket_service.create_ticket(db, board_id, user.user_id, body)

    return Response(status_code=status.HTTP_201_CREATED)