"""empty message

Revision ID: 3ebf4f1d3148
Revises: a2ae0d27805c
Create Date: 2021-11-10 12:45:54.534470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ebf4f1d3148'
down_revision = 'a2ae0d27805c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('programe', sa.String(length=4577), nullable=False),
    sa.Column('information', sa.Text(), nullable=True),
    sa.Column('uploaded', sa.DateTime(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('ends', sa.String(length=54), nullable=True),
    sa.Column('image', sa.Text(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('mimetype', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=333), nullable=False),
    sa.Column('discipline', sa.String(length=213), nullable=False),
    sa.Column('speaker', sa.String(length=163), nullable=False),
    sa.Column('img', sa.Text(), nullable=False),
    sa.Column('names', sa.Text(), nullable=False),
    sa.Column('mimetypes', sa.Text(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['Event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('image')
    op.drop_table('Event')
    # ### end Alembic commands ###
