"""add message to track_error

Revision ID: f331bc3e361c
Revises: c9eaa6f3f09c
Create Date: 2021-07-15 18:16:59.266778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f331bc3e361c'
down_revision = 'c9eaa6f3f09c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('track_error', sa.Column('message', sa.BLOB(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('track_error', 'message')
    # ### end Alembic commands ###
