"""Add new fields for user

Revision ID: 7d3413ca5e8d
Revises: af302421c6dc
Create Date: 2019-05-03 22:29:41.038719

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '7d3413ca5e8d'
down_revision = 'af302421c6dc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('user', sa.Column('email', sa.String(length=255), nullable=False))
    op.add_column('user', sa.Column('is_admin', sa.Boolean(), nullable=False))


def downgrade() -> None:
    op.drop_column('user', 'is_admin')
    op.drop_column('user', 'email')
