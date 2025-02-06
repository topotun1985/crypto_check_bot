"""add last_triggered_at column

Revision ID: add_last_triggered_at
Revises: merge_heads
Create Date: 2025-02-03 20:13:49.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_last_triggered_at'
down_revision = 'merge_heads'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('alerts', sa.Column('last_triggered_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column('alerts', 'last_triggered_at')
