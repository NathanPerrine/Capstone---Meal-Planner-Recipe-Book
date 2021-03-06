"""foreign key mealplan

Revision ID: 4cae4d8a12ca
Revises: 2e8f4930f495
Create Date: 2022-04-28 03:18:35.933035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cae4d8a12ca'
down_revision = '2e8f4930f495'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'my_meal_plan', 'recipe', ['recipe_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'my_meal_plan', type_='foreignkey')
    # ### end Alembic commands ###
