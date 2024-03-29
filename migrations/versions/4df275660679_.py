"""empty message

Revision ID: 4df275660679
Revises: 3f201ab531d5
Create Date: 2023-12-21 13:46:35.473215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4df275660679'
down_revision = '3f201ab531d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.TEXT(),
               type_=sa.String(length=2000),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.String(length=2000),
               type_=sa.TEXT(),
               existing_nullable=True)

    # ### end Alembic commands ###
