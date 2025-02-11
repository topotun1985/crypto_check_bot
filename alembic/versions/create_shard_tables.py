"""create shard tables

Revision ID: create_shard_tables
Revises: remove_unused_columns
Create Date: 2025-02-11 13:11:19.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'create_shard_tables'
down_revision: Union[str, None] = 'remove_unused_columns'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем таблицы в каждом шарде
    for shard_id in range(2):  # Начинаем с 2 шардов
        op.execute(f'CREATE DATABASE IF NOT EXISTS crypto_bot_shard_{shard_id}')
        
        # Переключаемся на базу данных шарда
        with op.get_bind().connect() as conn:
            conn.execute(f'USE crypto_bot_shard_{shard_id}')
            
            # Создаем все необходимые таблицы
            op.create_table(
                'users',
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('telegram_id', sa.BigInteger(), nullable=False),
                sa.Column('username', sa.String(length=70)),
                sa.Column('language', sa.String(), server_default='en'),
                sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
                sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
                sa.PrimaryKeyConstraint('id'),
                sa.UniqueConstraint('telegram_id')
            )

            op.create_table(
                'subscriptions',
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('user_id', sa.Integer(), nullable=True),
                sa.Column('plan', sa.String()),
                sa.Column('expires_at', sa.TIMESTAMP()),
                sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
                sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
                sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                sa.PrimaryKeyConstraint('id')
            )

            op.create_table(
                'user_currencies',
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('user_id', sa.Integer(), nullable=True),
                sa.Column('currency', sa.String(), nullable=False),
                sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
                sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
                sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                sa.PrimaryKeyConstraint('id'),
                sa.UniqueConstraint('user_id', 'currency', name='uix_user_currency')
            )

            op.create_table(
                'alerts',
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('user_id', sa.Integer(), nullable=True),
                sa.Column('user_currency_id', sa.Integer(), nullable=True),
                sa.Column('threshold', sa.DECIMAL(precision=18, scale=8), nullable=False),
                sa.Column('condition_type', sa.String(length=50), nullable=False, server_default='above'),
                sa.Column('currency_type', sa.String(length=10), nullable=False, server_default='USD'),
                sa.Column('is_active', sa.Boolean(), nullable=True),
                sa.Column('last_triggered_at', sa.TIMESTAMP()),
                sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
                sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
                sa.ForeignKeyConstraint(['user_currency_id'], ['user_currencies.id'], ondelete='CASCADE'),
                sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                sa.PrimaryKeyConstraint('id'),
                sa.UniqueConstraint('user_id', 'user_currency_id', 'condition_type', 'currency_type',
                                  name='uix_user_currency_alert_type')
            )


def downgrade() -> None:
    # При откате удаляем базы данных шардов
    for shard_id in range(2):
        op.execute(f'DROP DATABASE IF EXISTS crypto_bot_shard_{shard_id}')
