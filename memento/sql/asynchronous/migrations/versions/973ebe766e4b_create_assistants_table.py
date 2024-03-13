"""create assistants table

Revision ID: 973ebe766e4b
Revises: 9813b7d8df1a
Create Date: 2024-03-12 19:49:52.367423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '973ebe766e4b'
down_revision: Union[str, None] = '9813b7d8df1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "assistants",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(20), nullable=False, unique=True),
        sa.Column("system", sa.Text, nullable=False),
        sa.Column("model", sa.String(20)),
        sa.Column("tokens", sa.Integer),
    )


def downgrade() -> None:
    op.drop_table("assistants")
