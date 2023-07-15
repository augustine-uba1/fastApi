"""add content column to posts table

Revision ID: cf63dae101a3
Revises: d2e3460c48c7
Create Date: 2023-07-13 08:43:00.892240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf63dae101a3'
down_revision = 'd2e3460c48c7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass