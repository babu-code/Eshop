"""empty message

Revision ID: 78edde251f6f
Revises: e45e8f3c3b67
Create Date: 2023-12-28 12:03:49.819573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78edde251f6f'
down_revision = 'e45e8f3c3b67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('stock', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('stock')

    # ### end Alembic commands ###
