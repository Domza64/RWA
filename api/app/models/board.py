from __future__ import annotations

from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Board(Base):
    """
    Board koji sadrzi taskove

    Atributi:
        id:              Surrogate primary key.
        name:            Ime boarda.
        description:     Opis boarda.
    """

    __tablename__ = "boards"

    board_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(50), nullable=False)

    memberships: Mapped[List["BoardMembers"]] = relationship(
        "BoardMembers",
        back_populates="board"
    )

    workflow_stages: Mapped[List["WorkflowStage"]] = relationship(
        "WorkflowStage",
        back_populates="board"
    )