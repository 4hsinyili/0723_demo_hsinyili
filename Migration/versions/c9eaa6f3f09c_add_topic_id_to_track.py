"""add topic_id to track

Revision ID: c9eaa6f3f09c
Revises: d9c5a9e2eca4
Create Date: 2021-07-15 17:39:18.110105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9eaa6f3f09c'
down_revision = 'd9c5a9e2eca4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('track', sa.Column('topic_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('track', 'topic_id')
    # ### end Alembic commands ###
