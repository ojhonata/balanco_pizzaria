"""logica no difference na tabela balance_items 1

Revision ID: a87f25e1d5e8
Revises: e29d181824de
Create Date: 2026-07-20 16:58:39.097238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a87f25e1d5e8'
down_revision: Union[str, Sequence[str], None] = 'e29d181824de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('balance_items', 'difference')
    op.add_column('balance_items', sa.Column(
        'difference', sa.DECIMAL(11, 2),
        sa.Computed('expected_quantity - counted_quantity', persisted=True),
        nullable=False
    ))


def downgrade() -> None:
    op.drop_column('balance_items', 'difference')
    op.add_column('balance_items', sa.Column(
        'difference', sa.DECIMAL(11, 2),
        nullable=False
    ))
