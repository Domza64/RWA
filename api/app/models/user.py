from __future__ import annotations

from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class User(Base):
    """
    Korisnik sustava

    Atributi:
        user_id:       Surrogate primary key.
        username:      korisnicko ime (jedinstven u sustavu).
        email:         Login email (jedinstven u sustavu).
        password_hash: Bcrypt hash lozinke (NIKAD plain text).
    """

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    memberships: Mapped[List["BoardMembers"]] = relationship(
        "BoardMembers",
        back_populates="user"
    )

    assigned_tickets: Mapped[List["Ticket"]] = relationship(
        "Ticket",
        foreign_keys="Ticket.assignee_id",
        back_populates="assignee"
    )

    reported_tickets: Mapped[List["Ticket"]] = relationship(
        "Ticket",
        foreign_keys="Ticket.reporter_id",
        back_populates="reporter"
    )