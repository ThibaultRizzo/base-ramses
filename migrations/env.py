from logging.config import fileConfig

# from app import models
import os

from alembic import context
from sqlalchemy import engine_from_config, pool

from models.base_model import BaseModel

# from core.config import settings
# from core.utils.db.base_model import BaseModel


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseModel.metadata
# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# def get_url():
#     user = os.getenv("DB_USER", "test")
#     password = os.getenv("DB_PASSWORD", "test")
#     server = os.getenv("DB_HOST", "db")
#     db = os.getenv("DB_NAME", "ramses")
#     return f"postgresql://{user}:{password}@{server}/{db}"

url = os.getenv("SQLALCHEMY_DATABASE_URL", "postgresql://ramses:ramses@localhost:5445/ramses")


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # url = settings.get_database_uri()
    # url = f"postgresql://test:test@localhost/5434"

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    # configuration["sqlalchemy.url"] = settings.get_database_uri()
    configuration["sqlalchemy.url"] = url
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
