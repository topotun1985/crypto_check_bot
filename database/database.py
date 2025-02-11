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

from .sharding import ShardManager

# Инициализируем менеджер шардов
shard_manager = ShardManager()

# Создаём фабрику сессий
def create_session_factory(engine):
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Словарь для хранения фабрик сессий для каждого шарда
session_factories = {}

# Функция для создания таблиц в БД
async def create_db_and_tables():
    try:
        logger.info("Starting to create database tables in all shards...")
        for shard_id in range(shard_manager.shard_count):
            engine = await shard_manager.get_engine(shard_id)
            if engine is None:
                raise Exception(f"Failed to get engine for shard {shard_id}")
                
            async with engine.begin() as conn:
                logger.info(f"Creating database tables in shard {shard_id}...")
                await conn.run_sync(Base.metadata.create_all)
                logger.info(f"Database tables created successfully in shard {shard_id}")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise

@asynccontextmanager
async def get_db(user_id: int = None) -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии базы данных для конкретного шарда.
    Если user_id не указан, используется шард по умолчанию (0)."""
    logger.info(f"Getting database session for user_id: {user_id}")
    shard_id = shard_manager.get_shard_key(user_id) if user_id is not None else 0
    logger.info(f"Using shard {shard_id} for user {user_id}")
    
    if shard_id not in session_factories:
        logger.info(f"Creating new session factory for shard {shard_id}")
        engine = await shard_manager.get_engine(shard_id)
        if engine is None:
            logger.error(f"Failed to get engine for shard {shard_id}")
            raise Exception(f"Failed to get engine for shard {shard_id}")
        session_factories[shard_id] = create_session_factory(engine)
    
    async with session_factories[shard_id]() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            logger.error(f"Error in database session: {str(e)}")
            await session.rollback()
            raise e
