"""empty message

Revision ID: 62d61e2ecfda
Revises: 
Create Date: 2022-03-27 17:52:16.698816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62d61e2ecfda'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password_hash', sa.String(length=30), nullable=False),
    sa.Column('confirm', sa.Boolean(), nullable=True),
    sa.Column('about_me', sa.Text(), nullable=True),
    sa.Column('regist_date', sa.DateTime(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('User')
    # ### end Alembic commands ###
