"""First migration

Revision ID: 89acf99799d3
Revises: 
Create Date: 2024-07-22 16:22:41.287973

"""
import uuid

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '89acf99799d3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'driver_data',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('driver_id', sa.UUID(as_uuid=True), index=True),
        sa.Column('latitude', sa.Float),
        sa.Column('longitude', sa.Float),
        sa.Column('altitude', sa.Float),
        sa.Column('speed', sa.Float),
        sa.Column('is_correct', sa.Boolean),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Index('idx_driver_id', 'driver_id')
    )


def downgrade():
    op.drop_table('driver_data')
