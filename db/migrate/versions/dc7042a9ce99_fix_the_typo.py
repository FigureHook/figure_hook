"""fix the typo...

Revision ID: dc7042a9ce99
Revises: 3bd094f697e8
Create Date: 2021-05-15 07:14:44.381991

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import orm

from Models.relation_table import (product_paintwork_table,
                                   product_sculptor_table)

# revision identifiers, used by Alembic.
revision = 'dc7042a9ce99'
down_revision = '3bd094f697e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_paintwork', sa.Column('product_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'product_paintwork', 'product', ['product_id'], ['id'])
    op.add_column('product_sculptor', sa.Column('product_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'product_sculptor', 'product', ['product_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('product_paintwork_product_id_fkey', 'product_paintwork', type_='foreignkey')
    op.drop_constraint('product_sculptor_product_id_fkey', 'product_sculptor', type_='foreignkey')

    op.drop_column('product_sculptor', 'product_id')
    op.drop_column('product_paintwork', 'product_id')

    # ### end Alembic commands ###