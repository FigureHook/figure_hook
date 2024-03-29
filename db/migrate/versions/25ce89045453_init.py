"""init

Revision ID: 25ce89045453
Revises: 
Create Date: 2021-09-30 12:12:44.883813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25ce89045453'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('announcement_checksum',
    sa.Column('site', sa.Enum('GSC', 'ALTER', 'NATIVE', name='sourcesite'), nullable=False),
    sa.Column('checksum', sa.String(), nullable=True),
    sa.Column('checked_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('site')
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('company',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('paintwork',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('periodic_task',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('executed_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('sculptor',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('series',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('webhook',
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('channel_id', sa.String(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('is_existed', sa.Boolean(), nullable=True),
    sa.Column('is_nsfw', sa.Boolean(), nullable=True),
    sa.Column('lang', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('channel_id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('product',
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('size', sa.SmallInteger(), nullable=True),
    sa.Column('scale', sa.SmallInteger(), nullable=True),
    sa.Column('resale', sa.Boolean(), nullable=True),
    sa.Column('adult', sa.Boolean(), nullable=True),
    sa.Column('copyright', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('jan', sa.String(length=13), nullable=True),
    sa.Column('id_by_official', sa.String(), nullable=True),
    sa.Column('checksum', sa.String(length=32), nullable=True),
    sa.Column('order_period_start', sa.DateTime(timezone=True), nullable=True),
    sa.Column('order_period_end', sa.DateTime(timezone=True), nullable=True),
    sa.Column('thumbnail', sa.String(), nullable=True),
    sa.Column('og_image', sa.String(), nullable=True),
    sa.Column('series_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('manufacturer_id', sa.Integer(), nullable=True),
    sa.Column('releaser_id', sa.Integer(), nullable=True),
    sa.Column('distributer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['distributer_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['manufacturer_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['releaser_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['series_id'], ['series.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('jan')
    )
    op.create_table('product_official_image',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_paintwork',
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('paintwork_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['paintwork_id'], ['paintwork.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE')
    )
    op.create_table('product_release_info',
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('tax_including', sa.Boolean(), nullable=True),
    sa.Column('initial_release_date', sa.Date(), nullable=True),
    sa.Column('delay_release_date', sa.Date(), nullable=True),
    sa.Column('announced_at', sa.Date(), nullable=True),
    sa.Column('shipped_at', sa.Date(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_sculptor',
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('sculptor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sculptor_id'], ['sculptor.id'], ondelete='CASCADE')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_sculptor')
    op.drop_table('product_release_info')
    op.drop_table('product_paintwork')
    op.drop_table('product_official_image')
    op.drop_table('product')
    op.drop_table('webhook')
    op.drop_table('series')
    op.drop_table('sculptor')
    op.drop_table('periodic_task')
    op.drop_table('paintwork')
    op.drop_table('company')
    op.drop_table('category')
    op.drop_table('announcement_checksum')
    # ### end Alembic commands ###
