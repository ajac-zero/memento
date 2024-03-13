"""create messages table

Revision ID: 90849fb46e6c
Revises: 3958467249ad
Create Date: 2024-03-12 19:52:11.656559

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90849fb46e6c'
down_revision: Union[str, None] = '3958467249ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "conversation",
            sa.Integer,
            sa.ForeignKey("conversations.id"),
            nullable=False,
        ),
        sa.Column("role", sa.String(9), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("prompt", sa.Text, nullable=False),
        sa.Column("augment", sa.PickleType),
    )


def downgrade() -> None:
    op.drop_table("messages")
