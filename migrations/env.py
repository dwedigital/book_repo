import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic.config import Config
from app.database import Base
from app.models.models import Book, BookRecord, User

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = Config("alembic.ini")
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the config with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to config.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    config.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with config.begin_transaction():
        config.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        config.configure(connection=connection, target_metadata=target_metadata)

        with config.begin_transaction():
            config.run_migrations()


if config.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
