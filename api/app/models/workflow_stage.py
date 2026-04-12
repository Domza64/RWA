from __future__ import annotations

from typing import List

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class WorkflowStage(Base):
    """
    Reprezentira vertikalne redove npr. (TO DO, IN PROGRESS, DONE) na boardu.
    Admini boarda ih sami dodavaju, a članovi onda mogu stavljati tickete u workflow stageve.

    Atributi:
        stage_id:              Surrogate primary key.
        name:                  Ime workflow stagea.
        order:                 Redni broj za prikaz.
        board_id:              Board kojem pripada.
    """

    __tablename__ = "workflow_stage"

    stage_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    order: Mapped[int] = mapped_column(nullable=False)
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.board_id"), nullable=False)

    board: Mapped["Board"] = relationship(
        "Board", back_populates="workflow_stages")

    __table_args__ = (
        UniqueConstraint("board_id", "order"),
    )

    tickets: Mapped[List["Ticket"]] = relationship(
        "Ticket",
        foreign_keys="Ticket.stage_id",
        back_populates="current_stage"
    )