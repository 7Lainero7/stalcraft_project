from sqlalchemy import text

from database import BaseModel, engine, DB_SCHEMA


async def init_db():
    """
    Инициализация базы данных: создание всех таблиц и схемы.
    """
    async with engine.begin() as conn:
        await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {DB_SCHEMA}"))
        await conn.run_sync(BaseModel.metadata.create_all)
