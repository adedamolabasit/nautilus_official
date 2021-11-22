"""empty message

Revision ID: 52fb161c5232
Revises: a29bc2c92493
Create Date: 2021-11-21 17:26:42.163959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52fb161c5232'
down_revision = 'a29bc2c92493'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Event', sa.Column('host', sa.String(length=35), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Event', 'host')
    # ### end Alembic commands ###
