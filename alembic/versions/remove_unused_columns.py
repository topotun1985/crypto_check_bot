"""remove unused columns

Revision ID: remove_unused_columns
Revises: d661d7323fda
Create Date: 2025-02-11 12:42:32.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'remove_unused_columns'
down_revision: Union[str, None] = 'd661d7323fda'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Удаляем неиспользуемые столбцы
    op.drop_column('alerts', 'in_rub')
    op.drop_column('crypto_rates', 'previous_price')


def downgrade() -> None:
    # Восстанавливаем столбцы при откате
    op.add_column('alerts', sa.Column('in_rub', sa.Boolean(), nullable=True))
    op.add_column('crypto_rates', sa.Column('previous_price', sa.DECIMAL(precision=18, scale=8), nullable=True))
