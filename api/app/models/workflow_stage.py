from __future__ import annotations

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class WorkflowStage(Base):
    """
    Reprezentira vertikalne redove npr. (TO DO, IN PROGRESS, DONE) na boardu.
    Admini boarda ih sami dodavaju, a članovi onda mogu stavljati tickete u workflow stageve.

    Atributi:
        id:              Surrogate primary key.
        name:            Ime boarda.
        description:     Opis boarda.
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