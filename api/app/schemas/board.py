from typing import List
from pydantic import BaseModel, Field


class CreateBoardRequest(BaseModel):
    """Tijelo POST /boards requesta."""
    name: str = Field(min_length=1, max_length=30)
    description: str = Field(min_length=1, max_length=50)


class BoardDTO(BaseModel):
    board_id: int
    name: str
    description: str


class CreateBoardResponse(BaseModel):
    """Tijelo POST /boards responsea."""
    board_id: int


class BoardsResponse(BaseModel):
    """Odgovor s listom boardova za korisnika"""
    boards: List[BoardDTO]
