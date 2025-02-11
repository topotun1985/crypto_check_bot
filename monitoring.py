import logging
import time
from functools import wraps
from typing import Optional, Dict, Any
import asyncio
from sqlalchemy import text
from database.database import get_db

logger = logging.getLogger(__name__)

# Словарь для хранения метрик по шардам
shard_metrics: Dict[str, Dict[str, Any]] = {}

def init_shard_metrics():
    """Инициализирует метрики для каждого шарда."""
    for shard_id in range(2):  # Для 2 шардов
        shard_name = f"shard_{shard_id}"
        shard_metrics[shard_name] = {
            "query_count": 0,
            "total_query_time": 0.0,
            "avg_query_time": 0.0,
            "slow_queries": 0,
            "errors": 0,
            "last_error": None,
            "users_count": 0,
            "last_updated": None
        }

async def monitor_shards():
    """Периодически собирает метрики по шардам."""
    while True:
        try:
            for shard_id in range(2):
                user_id = shard_id  # Используем shard_id как user_id для правильного роутинга
                async with get_db(user_id=user_id) as session:
                    # Подсчет пользователей
                    result = await session.execute(text("SELECT COUNT(*) FROM users"))
                    users_count = result.scalar()

                    # Обновляем метрики
                    shard_name = f"shard_{shard_id}"
                    shard_metrics[shard_name].update({
                        "users_count": users_count,
                        "last_updated": time.time()
                    })

                    logger.info(f"Shard {shard_id} metrics updated: {shard_metrics[shard_name]}")

        except Exception as e:
            logger.error(f"Error monitoring shards: {e}")

        await asyncio.sleep(300)  # Обновляем каждые 5 минут

def track_query_metrics(shard_id: int, query_time: float, had_error: bool = False, error_msg: Optional[str] = None):
    """Отслеживает метрики запросов для конкретного шарда."""
    shard_name = f"shard_{shard_id}"
    metrics = shard_metrics.get(shard_name)
    
    if metrics:
        metrics["query_count"] += 1
        metrics["total_query_time"] += query_time
        metrics["avg_query_time"] = metrics["total_query_time"] / metrics["query_count"]
        
        if query_time > 1.0:  # Считаем медленным запрос более 1 секунды
            metrics["slow_queries"] += 1
        
        if had_error:
            metrics["errors"] += 1
            metrics["last_error"] = error_msg

def log_query_metrics(func):
    """Декоратор для логирования метрик запросов."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id is None:
            for arg in args:
                if isinstance(arg, int):
                    user_id = arg
                    break
        
        if user_id is None:
            logger.warning("No user_id found for query metrics tracking")
            return await func(*args, **kwargs)

        shard_id = user_id % 2  # Определяем шард
        start_time = time.time()
        error = None
        
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            error = str(e)
            raise
        finally:
            query_time = time.time() - start_time
            track_query_metrics(shard_id, query_time, had_error=bool(error), error_msg=error)
            
            if query_time > 1.0:
                logger.warning(f"Slow query detected in shard {shard_id}: {query_time:.2f}s")
    
    return wrapper

# Инициализируем метрики при импорте модуля
init_shard_metrics()
