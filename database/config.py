import logging
from os import getenv, path

from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

dotenv_path = find_dotenv()
if not dotenv_path:
    logging.warning('.env file not found')
else:
    load_dotenv(dotenv_path)

class Settings:
    DOMAIN = '127.0.0.1/'
    PORT = '8000'

    # DATABASE
    DB_HOST = getenv("DB_HOST", default='127.0.0.1')
    DB_PORT = getenv("DB_PORT", default='5432')
    DB_NAME = getenv("DB_NAME", default='postgres')
    DB_USER = getenv("DB_USER", default='postgres')
    DB_PASSWORD = getenv("DB_PASSWORD", default='postgres')
    DB_SCHEMA = getenv("DB_SCHEMA")

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    async def create_schema(self):
        engine = create_async_engine(self.DATABASE_URL, echo=True)
        async with engine.begin() as conn:
            await conn.run_sync(lambda conn: conn.execute(f"CREATE SCHEMA IF NOT EXISTS {self.DB_SCHEMA}"))
        await engine.dispose()

class ProductionSettings(Settings):
    DOMAIN = '?'  # заменить

class DevelopmentSettings(Settings):
    DB_HOST = '127.0.0.1'
    DB_PORT = 5432
    DB_NAME = 'postgres'
    DB_USER = 'postgres'
    DB_PASSWORD = 'qwer'

settings = {'development': DevelopmentSettings(), 'production': ProductionSettings()}

config_env = getenv('APP_ENV', default='testing')

if config_env not in settings.keys():
    raise SystemError('Неправильное значение переменной среды "APP_ENV"')

config = settings[config_env]

if config_env == 'production':
    logging.warning('Внимание, запускается продакшн, НЕ ДЛЯ РАЗРАБОТКИ!')
else:
    logging.warning('Внимание, запускается режим разработки!')

logging.warning(config.DATABASE_URL)