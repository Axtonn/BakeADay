"""Add Clerk identity fields to users

Revision ID: cc9c1a4e4c8b
Revises: b7c8aa9c9bbd
Create Date: 2025-02-12 18:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cc9c1a4e4c8b"
down_revision: Union[str, Sequence[str], None] = "b7c8aa9c9bbd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("clerk_id", sa.String(), nullable=True))
    op.add_column("users", sa.Column("phone", sa.String(), nullable=True))
    op.add_column("users", sa.Column("first_name", sa.String(), nullable=True))
    op.add_column("users", sa.Column("last_name", sa.String(), nullable=True))
    op.add_column("users", sa.Column("image_url", sa.String(), nullable=True))
    # Drop default, cast, then set default to avoid cast errors
    op.alter_column("users", "is_admin", server_default=None)
    op.alter_column(
        "users",
        "is_admin",
        existing_type=sa.Integer(),
        type_=sa.Boolean(),
        nullable=False,
        postgresql_using="is_admin::boolean",
    )
    op.alter_column(
        "users",
        "is_admin",
        server_default=sa.text("false"),
    )

    # Backfill clerk_id from email if missing (placeholder), then enforce not null/unique
    op.execute(
        """
        UPDATE users
        SET clerk_id = COALESCE(clerk_id, 'local-' || id)
        WHERE clerk_id IS NULL
        """
    )
    op.alter_column("users", "clerk_id", nullable=False)
    op.create_unique_constraint("uq_users_clerk_id", "users", ["clerk_id"])


def downgrade() -> None:
    op.drop_constraint("uq_users_clerk_id", "users", type_="unique")
    op.alter_column("users", "clerk_id", nullable=True)
    op.alter_column("users", "is_admin", existing_type=sa.Boolean(), type_=sa.Integer(), nullable=True, server_default=None)
    op.drop_column("users", "image_url")
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")
    op.drop_column("users", "phone")
    op.drop_column("users", "clerk_id")
