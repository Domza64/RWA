from __future__ import annotations

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class BoardMembers(Base):
    """
    Veza između boarda i članova

    Atributi:
        user_id (int): ID korisnika
        board_id (int): ID boarda
        role (str): Uloga korisnika na boardu
    """

    __tablename__ = "board_members"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), primary_key=True)
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.board_id"), primary_key=True)
    role: Mapped[str] = mapped_column(Text, nullable=False)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="memberships",
        foreign_keys=[user_id]
    )

    board: Mapped["Board"] = relationship(
        "Board",
        back_populates="memberships"
    )
