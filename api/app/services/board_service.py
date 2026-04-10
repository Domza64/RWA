from typing import List, Literal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.models.user import User
from app.repositories import board_repo, membership_repo
from app.schemas.board import BoardDTO, BoardUserResponse


async def get_boards(db: AsyncSession, user_id: int) -> List[BoardDTO]:
    """
    Vraća sve boardove za odredenog korisnika
    """
    boards = await board_repo.get_boards_for_user(db, user_id)

    return [board for board in boards]


async def create_board(db: AsyncSession, user: User, name: str, description: str) -> int:
    """Kreira novi board"""
    board_id = await board_repo.create_board(db, name, description, user)
    return board_id


async def get_members(db: AsyncSession, board_id: int, user_id: int) -> List[BoardUserResponse]:
    """Vraća listu članova"""
    has_access = await board_repo.user_has_access(db, user_id, board_id)
    if not has_access:
        raise AppError("forbidden", "You don't have access to this board", 403)

    members = await membership_repo.get_board_members(db, board_id)
    return [user_response for user_response in members]


async def add_member(db: AsyncSession, board_id: int, user: User, user_id: int, role: Literal["ADMIN", "MEMBER"]):
    """user je korisnik koji pokusava dodati, a user_id je id korisnika kojeg se dodaje kao membera"""
    has_access = await board_repo.user_has_admin_access(db, user.user_id, board_id)
    if not has_access:
        raise AppError("forbidden", "You can't add users to this board", 403)

    try:
        await membership_repo.add_membership(db, board_id, user_id, role)
    except IntegrityError:
        raise AppError("unable_to_add_user", "User with id {} already exists in board or not found".format(user_id), 400)
