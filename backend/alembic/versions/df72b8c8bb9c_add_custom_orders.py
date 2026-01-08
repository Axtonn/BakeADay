"""add custom_orders table

Revision ID: df72b8c8bb9c
Revises: cc9c1a4e4c8b
Create Date: 2025-12-12 15:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "df72b8c8bb9c"
down_revision: Union[str, Sequence[str], None] = "cc9c1a4e4c8b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "custom_orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("customer_name", sa.String(), nullable=False),
        sa.Column("customer_email", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("base_type", sa.String(), nullable=False),
        sa.Column("size", sa.String(), nullable=True),
        sa.Column("flavor", sa.String(), nullable=True),
        sa.Column("filling", sa.String(), nullable=True),
        sa.Column("topping", sa.String(), nullable=True),
        sa.Column("servings", sa.String(), nullable=True),
        sa.Column("delivery_type", sa.String(), nullable=True),
        sa.Column("requested_date", sa.String(), nullable=True),
        sa.Column("message", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_custom_orders_id", "custom_orders", ["id"])


def downgrade() -> None:
    op.drop_index("ix_custom_orders_id", table_name="custom_orders")
    op.drop_table("custom_orders")
