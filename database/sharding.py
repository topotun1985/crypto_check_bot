from typing import Dict, Optional
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
import logging
from database.repositories.alert_repository import AlertRepository

logger = logging.getLogger(__name__)

class ShardManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.shard_count = 5  # Начнем с 2 шардов
            self.engines: Dict[int, AsyncEngine] = {}
            self.alert_repository = AlertRepository(self)
            self.initialized = True
    
    def get_shard_key(self, user_id: int) -> int:
        """Определяет номер шарда на основе user_id"""
        shard_id = user_id % self.shard_count
        logger.info(f"User {user_id} mapped to shard {shard_id}")
        return shard_id
    
    async def get_engine(self, shard_id: int) -> Optional[AsyncEngine]:
        """Получает или создает подключение к нужному шарду"""
        if shard_id not in self.engines:
            try:
                # Формируем URL для конкретного шарда
                db_name = f"crypto_bot_shard_{shard_id}"
                url = f"postgresql+asyncpg://postgres:Vadim22021985@db:5432/{db_name}"
                
                self.engines[shard_id] = create_async_engine(
                    url,
                    echo=False,
                    pool_size=5,
                    max_overflow=10
                )
                logger.info(f"Created engine for shard {shard_id}")
            except Exception as e:
                logger.error(f"Error creating engine for shard {shard_id}: {e}")
                return None
                
        return self.engines[shard_id]
    
    async def get_all_engines(self) -> Dict[int, AsyncEngine]:
        """Получает список всех движков для всех шардов"""
        for shard_id in range(self.shard_count):
            if shard_id not in self.engines:
                await self.get_engine(shard_id)
        return self.engines

    async def get_session(self, shard_id: int):
        """Создает новую сессию для указанного шарда"""
        from sqlalchemy.ext.asyncio import AsyncSession
        from sqlalchemy.orm import sessionmaker

        engine = await self.get_engine(shard_id)
        if engine is None:
            raise ValueError(f"Could not get engine for shard {shard_id}")

        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        return async_session()
