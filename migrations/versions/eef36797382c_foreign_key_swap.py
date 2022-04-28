"""foreign key swap

Revision ID: eef36797382c
Revises: bc2d7232c74a
Create Date: 2022-04-28 12:48:01.952573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eef36797382c'
down_revision = 'bc2d7232c74a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('my_meal_plan', sa.Column('recipe_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'my_meal_plan', 'recipe', ['recipe_id'], ['id'])
    op.drop_constraint('recipe_meal_plan_id_fkey', 'recipe', type_='foreignkey')
    op.drop_column('recipe', 'meal_plan_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('meal_plan_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('recipe_meal_plan_id_fkey', 'recipe', 'my_meal_plan', ['meal_plan_id'], ['id'])
    op.drop_constraint(None, 'my_meal_plan', type_='foreignkey')
    op.drop_column('my_meal_plan', 'recipe_id')
    # ### end Alembic commands ###