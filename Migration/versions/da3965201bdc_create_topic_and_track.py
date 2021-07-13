"""create topic and track

Revision ID: da3965201bdc
Revises: 
Create Date: 2021-07-12 17:57:28.292878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da3965201bdc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('topic',
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('post_time', sa.DateTime(), nullable=True),
    sa.Column('stop_track', sa.DateTime(), nullable=True),
    sa.Column('post_by', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('url')
    )
    op.create_table('track',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('track_time', sa.DateTime(), nullable=True),
    sa.Column('view_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['url'], ['topic.url'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('track')
    op.drop_table('topic')
    # ### end Alembic commands ###