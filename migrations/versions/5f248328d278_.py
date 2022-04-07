"""empty message

Revision ID: 5f248328d278
Revises: a12dc9edf02e
Create Date: 2022-04-07 11:43:38.650235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f248328d278'
down_revision = 'a12dc9edf02e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('avatar_url', sa.String(length=30), server_default='/static/img/default.png', nullable=True))
    op.create_unique_constraint(None, 'User', ['avatar_url'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'User', type_='unique')
    op.drop_column('User', 'avatar_url')
    # ### end Alembic commands ###