"""empty message

Revision ID: 47207f7413c5
Revises: 624503a752d1
Create Date: 2023-09-23 14:05:20.463776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47207f7413c5'
down_revision: Union[str, None] = '624503a752d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(length=20), nullable=False))
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=False))
    op.add_column('users', sa.Column('email', sa.String(length=30), nullable=False))
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'email')
    op.drop_column('users', 'hashed_password')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###