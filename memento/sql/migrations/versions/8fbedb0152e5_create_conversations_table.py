"""create conversations table

Revision ID: 8fbedb0152e5
Revises: 0f36f68ad565
Create Date: 2024-02-20 09:33:22.210267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import Column


# revision identifiers, used by Alembic.
revision: str = "8fbedb0152e5"
down_revision: Union[str, None] = "0f36f68ad565"
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
