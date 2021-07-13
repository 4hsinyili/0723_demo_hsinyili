"""add tz to datetime columns in track

Revision ID: 6b58b7cd1329
Revises: e2180472f6d1
Create Date: 2021-07-12 21:21:08.887887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b58b7cd1329'
down_revision = 'e2180472f6d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('topic', 'post_time', type_=sa.DateTime(timezone=True))
    op.alter_column('topic', 'stop_track', type_=sa.Boolean)
    op.add_column('topic', sa.Column('stop_track_at', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('topic', 'stop_track_at')
    op.alter_column('topic', 'post_time', type_=sa.DateTime)
    op.alter_column('topic', 'stop_track', type_=sa.DateTime)
    # ### end Alembic commands ###
