"""Align schema with current models (slug, flags, numerics, timestamps)

Revision ID: b7c8aa9c9bbd
Revises: af96ed4ce7d6
Create Date: 2025-02-12 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b7c8aa9c9bbd"
down_revision: Union[str, Sequence[str], None] = "af96ed4ce7d6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Products table: slug/metadata + stricter types
    op.add_column("products", sa.Column("slug", sa.String(), nullable=True))
    op.add_column("products", sa.Column("category", sa.String(), nullable=True))
    op.add_column(
        "products",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )
    op.add_column(
        "products",
        sa.Column(
            "is_featured",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )
    op.add_column(
        "products",
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.add_column(
        "products",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.alter_column(
        "products",
        "price",
        existing_type=sa.Float(),
        type_=sa.Numeric(10, 2),
        existing_nullable=False,
    )
    op.alter_column(
        "products",
        "in_stock",
        existing_type=sa.Integer(),
        nullable=False,
        server_default="0",
    )
    # Backfill slug and enforce uniqueness
    op.execute(
        """
        UPDATE products
        SET slug = COALESCE(
            NULLIF(regexp_replace(lower(name), '[^a-z0-9]+', '-', 'g'), ''),
            'product'
        ) || '-' || id
        WHERE slug IS NULL
        """
    )
    op.alter_column("products", "slug", nullable=False)
    op.create_unique_constraint("uq_products_slug", "products", ["slug"])

    # Orders table: delivery metadata, numerics, status
    op.add_column("orders", sa.Column("delivery_type", sa.String(), nullable=True))
    op.add_column("orders", sa.Column("delivery_address", sa.String(), nullable=True))
    op.add_column(
        "orders", sa.Column("delivery_distance_km", sa.Float(), nullable=True)
    )
    op.add_column(
        "orders",
        sa.Column("delivery_fee", sa.Numeric(10, 2), nullable=True),
    )
    op.add_column(
        "orders",
        sa.Column(
            "status",
            sa.String(),
            nullable=False,
            server_default="pending_payment",
        ),
    )
    op.add_column("orders", sa.Column("scheduled_date", sa.DateTime(), nullable=True))
    op.alter_column(
        "orders",
        "customer_name",
        existing_type=sa.String(),
        nullable=False,
        server_default="",
    )
    op.alter_column(
        "orders",
        "customer_email",
        existing_type=sa.String(),
        nullable=False,
        server_default="",
    )
    op.alter_column(
        "orders",
        "total",
        existing_type=sa.Float(),
        type_=sa.Numeric(10, 2),
        nullable=False,
        server_default="0",
    )
    op.alter_column(
        "orders",
        "created_at",
        existing_type=sa.DateTime(),
        nullable=False,
        server_default=sa.text("now()"),
    )

    # Order items: stricter nullability and numeric price
    op.alter_column(
        "order_items",
        "order_id",
        existing_type=sa.Integer(),
        nullable=False,
    )
    op.alter_column(
        "order_items",
        "product_id",
        existing_type=sa.Integer(),
        nullable=False,
    )
    op.alter_column(
        "order_items",
        "quantity",
        existing_type=sa.Integer(),
        nullable=False,
    )
    op.alter_column(
        "order_items",
        "price",
        existing_type=sa.Float(),
        type_=sa.Numeric(10, 2),
        nullable=False,
        server_default="0",
    )

    # Reviews: ensure timestamps not null with default
    op.alter_column(
        "reviews",
        "created_at",
        existing_type=sa.DateTime(),
        nullable=False,
        server_default=sa.text("now()"),
    )

    # Users: default is_admin flag
    op.alter_column(
        "users",
        "is_admin",
        existing_type=sa.Integer(),
        nullable=False,
        server_default="0",
    )


def downgrade() -> None:
    # Users
    op.alter_column(
        "users",
        "is_admin",
        existing_type=sa.Integer(),
        nullable=True,
        server_default=None,
    )

    # Reviews
    op.alter_column(
        "reviews",
        "created_at",
        existing_type=sa.DateTime(),
        nullable=True,
        server_default=None,
    )

    # Order items
    op.alter_column(
        "order_items",
        "price",
        existing_type=sa.Numeric(10, 2),
        type_=sa.Float(),
        nullable=True,
        server_default=None,
    )
    op.alter_column(
        "order_items",
        "quantity",
        existing_type=sa.Integer(),
        nullable=True,
    )
    op.alter_column(
        "order_items",
        "product_id",
        existing_type=sa.Integer(),
        nullable=True,
    )
    op.alter_column(
        "order_items",
        "order_id",
        existing_type=sa.Integer(),
        nullable=True,
    )

    # Orders
    op.alter_column(
        "orders",
        "created_at",
        existing_type=sa.DateTime(),
        nullable=True,
        server_default=None,
    )
    op.alter_column(
        "orders",
        "total",
        existing_type=sa.Numeric(10, 2),
        type_=sa.Float(),
        nullable=True,
        server_default=None,
    )
    op.alter_column(
        "orders",
        "customer_email",
        existing_type=sa.String(),
        nullable=True,
        server_default=None,
    )
    op.alter_column(
        "orders",
        "customer_name",
        existing_type=sa.String(),
        nullable=True,
        server_default=None,
    )
    op.drop_column("orders", "scheduled_date")
    op.drop_column("orders", "status")
    op.drop_column("orders", "delivery_fee")
    op.drop_column("orders", "delivery_distance_km")
    op.drop_column("orders", "delivery_address")
    op.drop_column("orders", "delivery_type")

    # Products
    op.drop_constraint("uq_products_slug", "products", type_="unique")
    op.alter_column(
        "products",
        "in_stock",
        existing_type=sa.Integer(),
        nullable=True,
        server_default=None,
    )
    op.alter_column(
        "products",
        "price",
        existing_type=sa.Numeric(10, 2),
        type_=sa.Float(),
        existing_nullable=False,
    )
    op.drop_column("products", "updated_at")
    op.drop_column("products", "created_at")
    op.drop_column("products", "is_featured")
    op.drop_column("products", "is_active")
    op.drop_column("products", "category")
    op.drop_column("products", "slug")
