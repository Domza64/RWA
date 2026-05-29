from typing import List, Literal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.models.user import User
from app.repositories import board_repo, membership_repo
from app.schemas.board import BoardDTO, BoardUserResponse, WorkflowStageResponse


async def get_boards(db: AsyncSession, user_id: int) -> List[BoardDTO]:
    """
    Vraća sve boardove za odredenog korisnika
    """
    boards = await board_repo.get_boards_for_user(db, user_id)

    return [board for board in boards]


async def get_board(db: AsyncSession, board_id: int, user_id: int) -> BoardDTO:
    """
    Vraća board info
    """
    await check_read_access(db, board_id, user_id)
    
    board = await board_repo.get_board(db, board_id)
    return board


async def create_board(db: AsyncSession, user: User, name: str, description: str) -> int:
    """Kreira novi board"""
    board_id = await board_repo.create_board(db, name, description, user)
    return board_id


async def get_members(db: AsyncSession, board_id: int, user_id: int) -> List[BoardUserResponse]:
    """Vraća listu članova"""
    await check_read_access(db, board_id, user_id)

    members = await membership_repo.get_board_members(db, board_id)
    return [user_response for user_response in members]


async def add_member(db: AsyncSession, board_id: int, user: User, user_id: int, role: Literal["ADMIN", "MEMBER"]):
    """user je korisnik koji pokusava dodati, a user_id je id korisnika kojeg se dodaje kao membera"""
    await check_admin_access(db, user.user_id, board_id)

    try:
        await membership_repo.add_membership(db, board_id, user_id, role)
    except IntegrityError:
        # TODO: More specific error?
        raise AppError("unable_to_add_user", "User: {} or board: {} not found or user already exists in the board members".format(user_id, board_id), 400)


async def add_workflow_stage(db, board_id, user, name):
    """Dodaje novi ticket status na board"""
    await check_admin_access(db, user.user_id, board_id)

    try:
        await board_repo.add_workflow_stage(db, board_id, name)
    except IntegrityError:
        raise AppError("unable_to_create_stage", "Board with this name already exists", 400)


async def get_workflow_stages(db, board_id, user_id) -> List[WorkflowStageResponse]:
    """Vraća listu workflow stageva na boardu"""
    await check_read_access(db, board_id, user_id)

    workflow_stages = await board_repo.get_workflow_stages(db, board_id)
    return workflow_stages

# ---- Helper funkcije ----

async def check_read_access(db: AsyncSession, board_id: int, user_id: int):
    has_access = await board_repo.user_has_access(db, user_id, board_id)
    if not has_access:
        raise AppError("forbidden", "You don't have access to this board", 403)


async def check_admin_access(db: AsyncSession, user_id: int, board_id: int):
    has_access = await board_repo.user_has_admin_access(db, user_id, board_id)
    if not has_access:
        raise AppError("forbidden", "You don't have admin rights to this board", 403)
