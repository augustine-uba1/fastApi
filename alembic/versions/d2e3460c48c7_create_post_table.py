"""create post table

Revision ID: d2e3460c48c7
Revises: 
Create Date: 2023-07-13 08:33:31.121314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2e3460c48c7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable= False,
                                       primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False) )
     
    pass


def downgrade():
    op.drop_table('posts')
    pass
