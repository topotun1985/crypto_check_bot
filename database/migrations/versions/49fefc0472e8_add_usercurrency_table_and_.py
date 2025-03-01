"""Add UserCurrency table and relationships 2

Revision ID: 49fefc0472e8
Revises: 15899945bbd2
Create Date: 2025-01-23 23:01:08.560252

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '49fefc0472e8'
down_revision: Union[str, None] = '15899945bbd2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alerts', sa.Column('user_currency_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'alerts', 'user_currencies', ['user_currency_id'], ['id'], ondelete='CASCADE')
    op.drop_column('alerts', 'is_active')
    op.drop_column('alerts', 'currency')
    op.drop_column('alerts', 'last_notification')
    op.drop_column('crypto_rates', 'last_update')
    op.drop_column('crypto_rates', 'price_rub')
    op.create_unique_constraint('uix_user_currency', 'user_currencies', ['user_id', 'currency'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uix_user_currency', 'user_currencies', type_='unique')
    op.add_column('crypto_rates', sa.Column('price_rub', sa.NUMERIC(precision=18, scale=8), autoincrement=False, nullable=True))
    op.add_column('crypto_rates', sa.Column('last_update', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('alerts', sa.Column('last_notification', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('alerts', sa.Column('currency', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('alerts', sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'alerts', type_='foreignkey')
    op.drop_column('alerts', 'user_currency_id')
    # ### end Alembic commands ###
