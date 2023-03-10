"""empty message

Revision ID: 78167b627223
Revises: 
Create Date: 2023-02-27 17:18:03.266303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78167b627223'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('is_muver', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('customer_profile',
    sa.Column('customer_id', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('current_address', sa.String(length=100), nullable=False),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('state', sa.String(length=100), nullable=False),
    sa.Column('zip_code', sa.Integer(), nullable=False),
    sa.Column('phone_number', sa.String(length=12), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('customer_id')
    )
    op.create_table('muver_profile',
    sa.Column('muver_id', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('current_address', sa.String(length=100), nullable=False),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('state', sa.String(length=100), nullable=False),
    sa.Column('zip_code', sa.Integer(), nullable=False),
    sa.Column('phone_number', sa.String(length=12), nullable=False),
    sa.Column('tokens_available', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('muver_id')
    )
    op.create_table('muving_jobs',
    sa.Column('job_id', sa.String(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('start_add', sa.String(length=100), nullable=False),
    sa.Column('start_housing_type', sa.String(length=100), nullable=False),
    sa.Column('start_floor_num', sa.Integer(), nullable=True),
    sa.Column('start_beds', sa.Integer(), nullable=False),
    sa.Column('start_baths', sa.Integer(), nullable=False),
    sa.Column('end_add', sa.String(length=100), nullable=False),
    sa.Column('end_housing_type', sa.String(length=100), nullable=True),
    sa.Column('end_floor_num', sa.Integer(), nullable=True),
    sa.Column('end_beds', sa.Integer(), nullable=False),
    sa.Column('end_baths', sa.Integer(), nullable=False),
    sa.Column('extra_add', sa.String(length=100), nullable=True),
    sa.Column('moving_date', sa.DateTime(), nullable=False),
    sa.Column('job_posted_time', sa.DateTime(), nullable=True),
    sa.Column('customer_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customer_profile.customer_id'], ),
    sa.PrimaryKeyConstraint('job_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('muving_jobs')
    op.drop_table('muver_profile')
    op.drop_table('customer_profile')
    op.drop_table('user')
    # ### end Alembic commands ###
