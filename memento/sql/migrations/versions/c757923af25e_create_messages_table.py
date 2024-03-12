"""create messages table

Revision ID: c757923af25e
Revises: 8fbedb0152e5
Create Date: 2024-02-20 10:00:15.767275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c757923af25e"
down_revision: Union[str, None] = "8fbedb0152e5"
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
        sa.Column("augment", sa.Text),
    )


def downgrade() -> None:
    op.drop_table("messages")
