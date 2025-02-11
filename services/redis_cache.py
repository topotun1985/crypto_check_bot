from redis import asyncio as aioredis
import json
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class RedisCache:
    _instance = None
    
    def __new__(cls, redis_url: str = "redis://redis:6379"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, redis_url: str = "redis://redis:6379"):
        """Инициализация Redis клиента"""
        if not hasattr(self, 'redis'):
            self.redis = aioredis.Redis.from_url(redis_url, decode_responses=True)
            self.default_expire = 30  # 30 секунд для курсов криптовалют

    async def get_crypto_rates(self) -> Optional[Dict[str, float]]:
        """Получает курсы криптовалют из кэша"""
        try:
            rates = await self.redis.get("crypto_rates")
            return json.loads(rates) if rates else None
        except Exception as e:
            logger.error(f"Failed to get crypto rates from Redis: {e}")
            return None

    async def set_crypto_rates(self, rates: Dict[str, float]) -> bool:
        """Сохраняет курсы криптовалют в кэш"""
        try:
            await self.redis.set(
                "crypto_rates",
                json.dumps(rates),
                ex=self.default_expire
            )
            return True
        except Exception as e:
            logger.error(f"Failed to set crypto rates in Redis: {e}")
            return False

    async def get_dollar_rate(self) -> Optional[float]:
        """Получает курс доллара из кэша"""
        try:
            rate = await self.redis.get("usd_rate")
            return float(rate) if rate else None
        except Exception as e:
            logger.error(f"Failed to get dollar rate from Redis: {e}")
            return None

    async def set_dollar_rate(self, rate: float) -> bool:
        """Сохраняет курс доллара в кэш"""
        try:
            await self.redis.set(
                "usd_rate",
                str(rate),
                ex=self.default_expire
            )
            return True
        except Exception as e:
            logger.error(f"Failed to set dollar rate in Redis: {e}")
            return False

    async def close(self):
        """Закрывает соединение с Redis"""
        await self.redis.close()
