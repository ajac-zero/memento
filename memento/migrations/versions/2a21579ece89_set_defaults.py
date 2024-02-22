"""set defaults

Revision ID: 2a21579ece89
Revises: c757923af25e
Create Date: 2024-02-20 10:29:01.263101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2a21579ece89"
down_revision: Union[str, None] = "c757923af25e"
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
