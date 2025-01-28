from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from database.models import Base
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем параметры подключения из переменных окружения
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "Vadim22021985")
DB_NAME = os.getenv("POSTGRES_DB", "crypto_bot")
DB_HOST = os.getenv("POSTGRES_HOST", "db")  # используем имя сервиса из docker-compose
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

# Формируем URL для подключения
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

logger.info(f"Using database URL: {DATABASE_URL}")

# Создаём движок и сессию
try:
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    logger.info("Successfully created database engine")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

# Функция для создания таблиц в БД
async def create_db_and_tables():
    try:
        logger.info("Starting to create database tables...")
        async with engine.begin() as conn:
            logger.info("Creating database tables...")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise

@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии базы данных."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
