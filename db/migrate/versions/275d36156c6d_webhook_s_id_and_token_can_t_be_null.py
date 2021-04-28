"""webhook's id and token can't be null

Revision ID: 275d36156c6d
Revises: ec698af7e1d7
Create Date: 2021-04-28 15:43:56.396792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '275d36156c6d'
down_revision = 'ec698af7e1d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('webhook', 'id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('webhook', 'token',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('webhook', 'token',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('webhook', 'id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
