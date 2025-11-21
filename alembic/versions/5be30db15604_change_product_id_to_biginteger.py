"""Change product_id to BigInteger

Revision ID: 5be30db15604
Revises: e664ea53c26f
Create Date: 2025-11-21 23:51:46.507777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5be30db15604'
down_revision: Union[str, Sequence[str], None] = 'e664ea53c26f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Change product_id from INTEGER → BIGINT
    op.alter_column(
        'products',
        'product_id',
        existing_type=sa.Integer(),
        type_=sa.BigInteger(),
        existing_nullable=False
    )


def downgrade():
    # Reverse if you roll back the migration
    op.alter_column(
        'products',
        'product_id',
        existing_type=sa.BigInteger(),
        type_=sa.Integer(),
        existing_nullable=False
    )