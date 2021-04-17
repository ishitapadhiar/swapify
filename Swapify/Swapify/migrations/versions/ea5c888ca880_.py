"""added song length

Revision ID: ea5c888ca880
Revises: d12a3744e77f
Create Date: 2021-04-06 21:43:14.518588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea5c888ca880'
down_revision = 'd12a3744e77f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('song', sa.Column('length', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('song', 'length')
    # ### end Alembic commands ###