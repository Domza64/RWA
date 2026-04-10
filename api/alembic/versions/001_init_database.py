"""init clubs and users

Revision ID: 001
Revises:
Create Date: 2026-09-04

Prva migracija — kreira tablice clubs i users.

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

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # -------------------
    # users
    # -------------------
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("username", sa.Text(), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("password", sa.Text(), nullable=False),
    )

    # -------------------
    # board
    # -------------------
    op.create_table(
        "board",
        sa.Column("board_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
    )

    # -------------------
    # ticket_status
    # -------------------
    op.create_table(
        "ticket_status",
        sa.Column("status_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("status_text", sa.Text(), nullable=False),
        sa.Column("board_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["board_id"], ["board.board_id"]),
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
        sa.ForeignKeyConstraint(["board_id"], ["board.board_id"]),
    )

    # -------------------
    # ticket
    # -------------------
    op.create_table(
        "ticket",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("asignee", sa.Integer(), nullable=True),
        sa.Column("reporter", sa.Integer(), nullable=False),
        sa.Column("board_id", sa.Integer(), nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=True),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("type", sa.Text(), nullable=False),

        sa.ForeignKeyConstraint(["asignee"], ["users.user_id"]),
        sa.ForeignKeyConstraint(["reporter"], ["users.user_id"]),
        sa.ForeignKeyConstraint(["board_id"], ["board.board_id"]),
        sa.ForeignKeyConstraint(["status_id"], ["ticket_status.status_id"]),
    )


def downgrade() -> None:
    op.drop_table("ticket")
    op.drop_table("board_members")
    op.drop_table("ticket_status")
    op.drop_table("board")
    op.drop_table("users")
    