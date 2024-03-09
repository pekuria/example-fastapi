"""add users table

Revision ID: 7838396746cd
Revises: 0858bc435d98
Create Date: 2024-03-08 15:21:31.323911

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7838396746cd'
down_revision: Union[str, None] = '0858bc435d98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=True, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False,),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
