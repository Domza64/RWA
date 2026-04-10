from typing import List, Literal
from pydantic import BaseModel, Field

from app.schemas.auth import UserResponse


class CreateBoardRequest(BaseModel):
    """Tijelo POST /boards requesta."""
    name: str = Field(min_length=1, max_length=30)
    description: str = Field(min_length=1, max_length=50)


class BoardDTO(BaseModel):
    board_id: int
    name: str
    description: str

    model_config = {"from_attributes": True}


class CreateBoardResponse(BaseModel):
    """Tijelo POST /boards responsea."""
    board_id: int


class BoardsResponse(BaseModel):
    """Odgovor s listom boardova za korisnika"""
    boards: List[BoardDTO]


class AddUserRequest(BaseModel):
    """Tijelo POST /{board_id}/members/add requesta."""
    user_id: int
    role: Literal["ADMIN", "MEMBER"]


class BoardUserResponse(BaseModel):
    role: str
    user: UserResponse

    model_config = {"from_attributes": True}