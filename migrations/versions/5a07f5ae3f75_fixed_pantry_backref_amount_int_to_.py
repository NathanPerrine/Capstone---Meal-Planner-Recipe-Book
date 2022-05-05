"""fixed pantry backref, amount int to string

Revision ID: 5a07f5ae3f75
Revises: d0884573d136
Create Date: 2022-05-04 22:51:48.622475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a07f5ae3f75'
down_revision = 'd0884573d136'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('my_pantry', 'pantryAmount',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=15),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('my_pantry', 'pantryAmount',
               existing_type=sa.String(length=15),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
