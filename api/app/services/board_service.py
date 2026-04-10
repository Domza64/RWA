from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories import board_repo
from app.schemas.board import BoardDTO


async def get_boards(db: AsyncSession, user_id: int) -> List[BoardDTO]:
    """
    Vraća sve boardove za odredenog korisnika
    """
    boards = await board_repo.get_boards_for_user(db, user_id)

    return [
        BoardDTO(
            board_id=b.board_id,
            name=b.name,
            description=b.description,
        )
        for b in boards
    ]


async def create_board(db: AsyncSession, user: User, name: str, description: str) -> int:
    """Kreira novi board"""
    board_id = await board_repo.create_board(db, name, description, user)
    return board_id
