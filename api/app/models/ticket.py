from datetime import date
from sqlalchemy import String, Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Ticket(Base):
    """
    Model za ticket.

    Atributi:
        ticket_id: ID ticketa.
        title: Naslov.
        description: Opis.
        due_date: Rok (datum, može biti NULL).
        urgency: Prioritet (1-5).
        order: Redoslijed u stupcu.
        assignee_id: Dodijeljeni korisnik (nullable).
        reporter_id: Autor ticketa.
        board_id: ID boarda.
        stage_id: ID stupca (nullable).
    """

    __tablename__ = "tickets"

    ticket_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(400), nullable=False)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    urgency: Mapped[int] = mapped_column(Integer(), nullable=False)
    board_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.user_id"), nullable=True)
    reporter_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    stage_id: Mapped[int | None] = mapped_column(ForeignKey("workflow_stage.stage_id"), nullable=True)

    assignee: Mapped["User"] = relationship(
        "User",
        foreign_keys=[assignee_id],
        back_populates="assigned_tickets"
    )

    reporter: Mapped["User"] = relationship(
        "User",
        foreign_keys=[reporter_id],
        back_populates="reported_tickets"
    )

    current_stage: Mapped["WorkflowStage"] = relationship(
        "WorkflowStage",
        foreign_keys=[stage_id],
        back_populates="tickets"
    )
