from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import deps
from app.core.deps import get_db
from app.models import User
from app.schemas.board import CreateBoardRequest, BoardsResponse, CreateBoardResponse
from app.services import board_service

router = APIRouter()


@router.get("/", response_model=BoardsResponse)
async def get_boards(db: AsyncSession = Depends(get_db), user: User = Depends(deps.get_current_user)):
    """Vraća listu boardova korisnika."""
    boards = await board_service.get_boards(db, user.user_id)

    return BoardsResponse(boards=boards)


@router.post("/", response_model=CreateBoardResponse)
async def create_board(body: CreateBoardRequest, db: AsyncSession = Depends(get_db), user: User = Depends(deps.get_current_user)):
    """Kreira novi board"""
    board_id = await board_service.create_board(db, user, body.name, body.description)
    return CreateBoardResponse(board_id=board_id)

