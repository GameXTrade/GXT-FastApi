"""Add new column2

Revision ID: d800be8efd6a
Revises: e435ffae50be
Create Date: 2024-05-18 22:14:45.738297

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd800be8efd6a'
down_revision: Union[str, None] = 'e435ffae50be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('download_count', sa.Integer(), nullable=True, server_default="0"))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('items', 'download_count')
    # ### end Alembic commands ###
