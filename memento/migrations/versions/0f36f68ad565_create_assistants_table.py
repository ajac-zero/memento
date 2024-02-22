"""create assistants table

Revision ID: 0f36f68ad565
Revises: b2cc607acc45
Create Date: 2024-02-19 23:37:27.170202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0f36f68ad565"
down_revision: Union[str, None] = "b2cc607acc45"
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
