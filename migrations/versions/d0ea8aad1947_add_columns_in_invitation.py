"""Add columns in invitation

Revision ID: d0ea8aad1947
Revises: a9661794a1ad
Create Date: 2019-05-05 15:57:04.064282

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd0ea8aad1947'
down_revision = 'a9661794a1ad'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('invitation', sa.Column('expires', sa.DateTime(), nullable=False))
    op.create_unique_constraint('uq_invitation_email', 'invitation', ['email'])
    op.create_unique_constraint('uq_invitation_token', 'invitation', ['token'])


def downgrade() -> None:
    op.drop_constraint('uq_invitation_token', 'invitation', type_='unique')
    op.drop_constraint('uq_invitation_email', 'invitation', type_='unique')
    op.drop_column('invitation', 'expires')
