"""init database

Revision ID: 001
Revises:
Create Date: 2026-10-04

Prva migracija — kreira inicijalne potrebne tablice.

Što radi upgrade():
  1. Kreira inicijalne tablice

Što radi downgrade():
  Briše sve tablice, određenim redosljedom zbog FK.

NAPOMENA: Uvijek pročitaj migraciju prije pokretanja "alembic upgrade"!
Autogenerate može pogriješiti (npr. rename → drop+create).
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # -------------------
    # users
    # -------------------
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("username", sa.Text(), nullable=False, unique=True),
        sa.Column("email", sa.Text(), nullable=False, unique=True),
        sa.Column("password_hash", sa.Text(), nullable=False),
    )

    # -------------------
    # board
    # -------------------
    op.create_table(
        "boards",
        sa.Column("board_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
    )

    # -------------------
    # workflow_stage
    # -------------------
    op.create_table(
        "workflow_stage",
        sa.Column("stage_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("board_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["board_id"], ["boards.board_id"]),
        sa.UniqueConstraint("board_id", "order"),
        sa.UniqueConstraint("board_id", "name"),
    )

    # -------------------
    # board_members (COMPOSITE PK)
    # -------------------
    op.create_table(
        "board_members",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("board_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.Text(), nullable=False),

        sa.PrimaryKeyConstraint("board_id", "user_id"),

        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.ForeignKeyConstraint(["board_id"], ["boards.board_id"]),
    )

    # -------------------
    # ticket
    # -------------------
    op.create_table(
        "tickets",
        sa.Column("ticket_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("urgency", sa.Integer(), nullable=True),
        sa.Column("assignee_id", sa.Integer(), nullable=True),
        sa.Column("reporter_id", sa.Integer(), nullable=False),
        sa.Column("board_id", sa.Integer(), nullable=False),
        sa.Column("stage_id", sa.Integer(), nullable=True),

        sa.CheckConstraint("urgency >= 1 AND urgency <= 5", name="urgency_range_check"),
        sa.UniqueConstraint("board_id", "stage_id"),

        sa.ForeignKeyConstraint(["assignee_id"], ["users.user_id"]),
        sa.ForeignKeyConstraint(["reporter_id"], ["users.user_id"]),
        sa.ForeignKeyConstraint(["board_id"], ["boards.board_id"]),
        sa.ForeignKeyConstraint(["stage_id"], ["workflow_stage.stage_id"]),
    )


def downgrade() -> None:
    op.drop_table("tickets")
    op.drop_table("board_members")
    op.drop_table("workflow_stage")
    op.drop_table("boards")
    op.drop_table("users")
    