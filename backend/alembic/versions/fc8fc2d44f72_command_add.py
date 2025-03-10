"""command_add

Revision ID: fc8fc2d44f72
Revises: 92306ff20ea0
Create Date: 2024-12-02 14:58:13.529876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc8fc2d44f72'
down_revision: Union[str, None] = '92306ff20ea0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('command',
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('command', sa.Text(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('command')
    )
    op.create_index(op.f('ix_command_name'), 'command', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_command_name'), table_name='command')
    op.drop_table('command')
    # ### end Alembic commands ###
