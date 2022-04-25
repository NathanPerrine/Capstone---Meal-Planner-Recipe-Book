"""Added fields to Recipe table, reference, time, makes

Revision ID: f8ae18d53b2f
Revises: 75e360c469f7
Create Date: 2022-04-21 16:34:51.162294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8ae18d53b2f'
down_revision = '75e360c469f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('makes', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recipe', 'makes')
    # ### end Alembic commands ###