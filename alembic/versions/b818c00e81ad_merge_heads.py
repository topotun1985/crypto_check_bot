"""merge_heads

Revision ID: b818c00e81ad
Revises: add_last_triggered_at, create_shard_tables
Create Date: 2025-02-11 10:16:11.507336

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b818c00e81ad'
down_revision: Union[str, None] = ('add_last_triggered_at', 'create_shard_tables')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
