"""set defaults

Revision ID: 2bc8a95cfc82
Revises: 90849fb46e6c
Create Date: 2024-03-12 19:52:53.772956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bc8a95cfc82'
down_revision: Union[str, None] = '90849fb46e6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("INSERT INTO users VALUES (1, 'user')")
    op.execute(
        "INSERT INTO assistants VALUES (1, 'assistant', 'You are a helpful assistant', Null, Null)"
    )


def downgrade() -> None:
    op.execute("DELETE FROM users WHERE (id = 1)")
    op.execute("DELETE FROM assistants WHERE (id = 1)")
