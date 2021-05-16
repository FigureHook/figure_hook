"""cascade delete worker relationship

Revision ID: 005ff8428793
Revises: ab0b2fcfdf04
Create Date: 2021-05-16 04:50:56.296705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005ff8428793'
down_revision = 'ab0b2fcfdf04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('product_paintwork_paintwork_id_fkey', 'product_paintwork', type_='foreignkey')
    op.drop_constraint('product_paintwork_product_id_fkey', 'product_paintwork', type_='foreignkey')
    op.create_foreign_key(None, 'product_paintwork', 'paintwork', ['paintwork_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'product_paintwork', 'product', ['product_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('product_sculptor_product_id_fkey', 'product_sculptor', type_='foreignkey')
    op.drop_constraint('product_sculptor_sculptor_id_fkey', 'product_sculptor', type_='foreignkey')
    op.create_foreign_key(None, 'product_sculptor', 'sculptor', ['sculptor_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'product_sculptor', 'product', ['product_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product_sculptor', type_='foreignkey')
    op.drop_constraint(None, 'product_sculptor', type_='foreignkey')
    op.create_foreign_key('product_sculptor_sculptor_id_fkey', 'product_sculptor', 'sculptor', ['sculptor_id'], ['id'])
    op.create_foreign_key('product_sculptor_product_id_fkey', 'product_sculptor', 'product', ['product_id'], ['id'])
    op.drop_constraint(None, 'product_paintwork', type_='foreignkey')
    op.drop_constraint(None, 'product_paintwork', type_='foreignkey')
    op.create_foreign_key('product_paintwork_product_id_fkey', 'product_paintwork', 'product', ['product_id'], ['id'])
    op.create_foreign_key('product_paintwork_paintwork_id_fkey', 'product_paintwork', 'paintwork', ['paintwork_id'], ['id'])
    # ### end Alembic commands ###