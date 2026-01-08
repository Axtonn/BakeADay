from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from app.core.config import settings
from app.core.db import Base  # your declarative base
from app.models import product, order, user, review, custom_order  # import so Alembic sees them


# Alembic Config object, provides access to values in alembic.ini
config = context.config

# Set up Python logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Tell Alembic about all your models for autogenerate support
target_metadata = Base.metadata


def get_sync_url() -> str:
    """
    Return a **synchronous** database URL for Alembic, derived from settings.DATABASE_URL.

    We run the app with an async URL (e.g. postgresql+asyncpg://...), but Alembic's
    migration engine is sync by default, so we strip the async driver.
    """
    url = settings.DATABASE_URL

    # Heroku-style / generic postgres
    if url.startswith("postgres://"):
        # normalize to SQLAlchemy's preferred 'postgresql://' first
        url = url.replace("postgres://", "postgresql://", 1)

    # Async driver → sync driver for migrations
    if url.startswith("postgresql+asyncpg://"):
        url = url.replace("postgresql+asyncpg://", "postgresql://", 1)

    # If you ever used a different async driver, convert it here similarly.

    return url


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine.
    Calls to context.execute() here emit the given SQL to the output.
    """
    url = get_sync_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we create an Engine and associate a connection with the context.
    """
    connectable = create_engine(
        get_sync_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
