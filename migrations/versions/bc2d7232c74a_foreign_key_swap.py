"""foreign key swap

Revision ID: bc2d7232c74a
Revises: 0171883282fa
Create Date: 2022-04-28 12:37:35.803904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc2d7232c74a'
down_revision = '0171883282fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('my_meal_plan_recipe_id_fkey', 'my_meal_plan', type_='foreignkey')
    op.drop_column('my_meal_plan', 'recipe_id')
    op.add_column('recipe', sa.Column('meal_plan_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'recipe', 'my_meal_plan', ['meal_plan_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'recipe', type_='foreignkey')
    op.drop_column('recipe', 'meal_plan_id')
    op.add_column('my_meal_plan', sa.Column('recipe_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('my_meal_plan_recipe_id_fkey', 'my_meal_plan', 'recipe', ['recipe_id'], ['id'])
    # ### end Alembic commands ###