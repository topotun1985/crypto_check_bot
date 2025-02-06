"""merge heads

Revision ID: merge_heads
Revises: add_alert_condition_columns, d661d7323fda
Create Date: 2025-02-03 20:02:29.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'merge_heads'
down_revision = ('add_alert_condition_columns', 'd661d7323fda')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
