"""add delivery fields to custom_orders

Revision ID: 1f3a2c44c1aa
Revises: df72b8c8bb9c
Create Date: 2025-12-12 15:20:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "1f3a2c44c1aa"
down_revision: Union[str, Sequence[str], None] = "df72b8c8bb9c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("custom_orders", sa.Column("delivery_address", sa.String(), nullable=True))
    op.add_column("custom_orders", sa.Column("delivery_distance_km", sa.Float(), nullable=True))
    op.add_column("custom_orders", sa.Column("delivery_fee", sa.Numeric(10, 2), nullable=True))


def downgrade() -> None:
    op.drop_column("custom_orders", "delivery_fee")
    op.drop_column("custom_orders", "delivery_distance_km")
    op.drop_column("custom_orders", "delivery_address")
