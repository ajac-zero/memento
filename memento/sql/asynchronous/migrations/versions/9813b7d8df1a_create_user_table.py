"""create user table

Revision ID: 9813b7d8df1a
Revises:
Create Date: 2024-03-12 19:48:29.321256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9813b7d8df1a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(30), nullable=False, unique=True),
    )


def downgrade() -> None:
    op.drop_table("users")
