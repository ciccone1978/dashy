"""Add user first/last name & registration date

Revision ID: e2cec88b98a3
Revises: 
Create Date: 2022-08-05 12:28:30.488134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2cec88b98a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('firstname', sa.String(length=64), nullable=True))
    op.add_column('Users', sa.Column('lastname', sa.String(length=64), nullable=True))
    op.add_column('Users', sa.Column('registration_date', sa.DateTime(), nullable=True))
    op.add_column('Users', sa.Column('password_change_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Users', 'password_change_date')
    op.drop_column('Users', 'registration_date')
    op.drop_column('Users', 'lastname')
    op.drop_column('Users', 'firstname')
    # ### end Alembic commands ###