"""create conversations table

Revision ID: 3958467249ad
Revises: 973ebe766e4b
Create Date: 2024-03-12 19:50:49.031184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3958467249ad'
down_revision: Union[str, None] = '973ebe766e4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "conversations",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text),
        sa.Column("user", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "assistant", sa.Integer, sa.ForeignKey("assistants.id"), nullable=False
        ),
    )


def downgrade() -> None:
    op.drop_table("conversations")
