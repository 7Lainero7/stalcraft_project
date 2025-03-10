from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from database.config import config

# URL для подключения к PostgreSQL
DATABASE_URL = config.DATABASE_URL
DB_SCHEMA = config.DB_SCHEMA

# Создание асинхронного движка
engine = create_async_engine(DATABASE_URL, echo=True)

# Сессия для взаимодействия с базой данных
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовый класс для моделей
metadata_obj = MetaData(schema=DB_SCHEMA)
BaseModel = declarative_base(metadata=metadata_obj)

# Функция для получения сессии
async def get_db():
    async with async_session() as session:
        yield session
