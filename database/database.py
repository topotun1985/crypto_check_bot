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

# Создаем URL для подключения к базе данных
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создаем движок базы данных
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    # Оптимизированные настройки пула для 30,000 пользователей
    pool_size=20,           # Базовый размер пула
    max_overflow=30,        # Максимальное количество дополнительных соединений
    pool_timeout=30,        # Таймаут ожидания соединения из пула
    pool_recycle=1800,      # Переподключение каждые 30 минут
    pool_pre_ping=True      # Проверка соединения перед использованием
)

# Создаём фабрику сессий
session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Функция для создания таблиц в БД
async def create_db_and_tables():
    try:
        logger.info("Creating database tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise

@asynccontextmanager
async def get_db(telegram_id: int = None) -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии базы данных.
    
    Args:
        telegram_id: Optional[int] - ID пользователя в Telegram для определения шарда
    """
    async with session_factory() as session:
        try:
            # TODO: Implement sharding logic here if needed
            # For now, we use a single database, so telegram_id is not used
            yield session
            await session.commit()
        except Exception as e:
            logger.error(f"Error in database session: {str(e)}")
            await session.rollback()
            raise e
