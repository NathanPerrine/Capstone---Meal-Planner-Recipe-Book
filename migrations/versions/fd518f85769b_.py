"""empty message

Revision ID: fd518f85769b
Revises: 4cae4d8a12ca
Create Date: 2022-04-28 11:26:05.425714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd518f85769b'
down_revision = '4cae4d8a12ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('my_meal_plan_recipe_id_fkey', 'my_meal_plan', type_='foreignkey')
    op.create_foreign_key(None, 'my_meal_plan', 'recipe', ['recipe_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'my_meal_plan', type_='foreignkey')
    op.create_foreign_key('my_meal_plan_recipe_id_fkey', 'my_meal_plan', 'recipe', ['recipe_id'], ['id'])
    # ### end Alembic commands ###
