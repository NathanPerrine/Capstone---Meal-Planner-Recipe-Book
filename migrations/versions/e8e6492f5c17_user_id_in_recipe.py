"""user_id in recipe

Revision ID: e8e6492f5c17
Revises: f8ae18d53b2f
Create Date: 2022-04-25 16:31:27.411305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8e6492f5c17'
down_revision = 'f8ae18d53b2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('my_recipes')
    op.add_column('recipe', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'recipe', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'recipe', type_='foreignkey')
    op.drop_column('recipe', 'user_id')
    op.create_table('my_recipes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('recipe_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], name='my_recipes_recipe_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='my_recipes_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='my_recipes_pkey')
    )
    # ### end Alembic commands ###
