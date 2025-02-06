"""add alert condition columns

Revision ID: add_alert_condition_columns
Revises: 
Create Date: 2025-02-03 20:02:29.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'add_alert_condition_columns'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('alerts')]
    
    # Add new columns if they don't exist
    if 'condition_type' not in columns:
        op.add_column('alerts', sa.Column('condition_type', sa.String(50), nullable=False, server_default='above'))
    if 'currency_type' not in columns:
        op.add_column('alerts', sa.Column('currency_type', sa.String(10), nullable=False, server_default='USD'))
    
    # Drop old columns if they exist
    if 'in_rub' in columns:
        op.drop_column('alerts', 'in_rub')
    if 'threshold_type' in columns:
        op.drop_column('alerts', 'threshold_type')


def downgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('alerts')]
    
    # Add back old columns if they don't exist
    if 'in_rub' not in columns:
        op.add_column('alerts', sa.Column('in_rub', sa.Boolean(), nullable=False, server_default='false'))
    if 'threshold_type' not in columns:
        op.add_column('alerts', sa.Column('threshold_type', sa.String(50), nullable=False, server_default='threshold'))
    
    # Drop new columns if they exist
    if 'condition_type' in columns:
        op.drop_column('alerts', 'condition_type')
    if 'currency_type' in columns:
        op.drop_column('alerts', 'currency_type')
