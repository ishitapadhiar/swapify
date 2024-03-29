"""empty message

Revision ID: 3d4c384f40a1
Revises: 
Create Date: 2021-03-16 19:18:48.594161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3d4c384f40a1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "artist",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("artist")
    # ### end Alembic commands ###
