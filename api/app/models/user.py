from __future__ import annotations

from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class User(Base):
    """
    Korisnik sustava

    Atributi:
        id:            Surrogate primary key.
        username:      korisnicko ime (jedinstven u sustavu).
        email:         Login email (jedinstven u sustavu).
        password_hash: Bcrypt hash lozinke (NIKAD plain text).
        boards:        List of boards
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
