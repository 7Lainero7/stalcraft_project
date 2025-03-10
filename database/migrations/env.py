from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context

from database import BaseModel, DATABASE_URL, DB_SCHEMA
from database.models import *
from database.utils import init_db

# Настройка логирования
config = context.config
fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", f"{DATABASE_URL}?async_fallback=True")

if config.config_file_name is not None:
    fileConfig(config.config_file_name)
# Указываем метаданные моделей
target_metadata = BaseModel.metadata



def run_migrations_offline():
    """
    Запуск миграций в оффлайн-режиме (без подключения к базе данных).
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"},
        version_table_schema=DB_SCHEMA
    )
    with context.begin_transaction():
        context.run_migrations()


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
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=DB_SCHEMA
        )

        with context.begin_transaction():
            context.run_migrations()



if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
