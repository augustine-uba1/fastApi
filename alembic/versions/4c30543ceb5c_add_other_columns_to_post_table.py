"""add other columns to post table

Revision ID: 4c30543ceb5c
Revises: cbd2de10fb31
Create Date: 2023-07-13 10:08:30.085010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c30543ceb5c'
down_revision = 'cbd2de10fb31'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published', sa.Boolean(),
                                    server_default='True', nullable=False),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, 
                                     server_default=sa.text('now()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
