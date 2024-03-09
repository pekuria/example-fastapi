"""add content column to post table

Revision ID: 0858bc435d98
Revises: 2a3fabedfdc9
Create Date: 2024-03-08 15:16:58.793187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0858bc435d98'
down_revision: Union[str, None] = '2a3fabedfdc9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
