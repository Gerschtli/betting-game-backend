"""Add invitation

Revision ID: a9661794a1ad
Revises: 7d3413ca5e8d
Create Date: 2019-05-03 22:56:58.324005

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'a9661794a1ad'
down_revision = '7d3413ca5e8d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'invitation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('is_admin', sa.Boolean(), nullable=False),
        sa.Column('token', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('invitation')
