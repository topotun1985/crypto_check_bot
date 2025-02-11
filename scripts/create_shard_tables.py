import asyncio
import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine
import logging

# Добавляем родительскую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.models import Base

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Параметры подключения
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "Vadim22021985")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

async def create_tables():
    """Создает таблицы в основной базе данных и шардах"""
    try:
        # Создаем таблицы в основной базе данных
        main_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/crypto_bot"
        main_engine = create_async_engine(main_url)
        
        logger.info("Creating tables in main database")
        async with main_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Tables created successfully in main database")
        
        # Создаем таблицы в каждом шарде
        for shard_id in range(2):  # Начинаем с 2 шардов
            db_name = f"crypto_bot_shard_{shard_id}"
            url = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{db_name}"
            
            engine = create_async_engine(url)
            
            logger.info(f"Creating tables in shard {shard_id}")
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info(f"Tables created successfully in shard {shard_id}")

    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(create_tables())
