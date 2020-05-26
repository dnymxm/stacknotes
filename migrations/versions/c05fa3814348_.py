"""empty message

Revision ID: c05fa3814348
Revises: 150d341bf95f
Create Date: 2020-05-26 09:30:11.816999

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c05fa3814348'
down_revision = '150d341bf95f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'notes', 'user', ['owner_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'notes', type_='foreignkey')
    op.drop_column('notes', 'owner_id')
    # ### end Alembic commands ###
