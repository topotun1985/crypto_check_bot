import time
import functools
import logging
from prometheus_client import Counter, Histogram
from typing import Callable, Any
from .prometheus_metrics import (
    REQUEST_LATENCY,
    DB_QUERY_LATENCY,
    ERROR_COUNTER,
    API_ERRORS
)

logger = logging.getLogger(__name__)

def track_request_latency(handler_name: str, shard: str = 'main') -> Callable:
    """Декоратор для отслеживания времени выполнения запросов"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                REQUEST_LATENCY.labels(
                    operation=handler_name,
                    shard=shard
                ).observe(duration)
                logger.info(f"Handler {handler_name} completed in {duration:.3f}s")
                return result
            except Exception as e:
                ERROR_COUNTER.labels(
                    error_type=type(e).__name__,
                    shard=shard
                ).inc()
                logger.error(f"Error in handler {handler_name}: {str(e)}")
                raise
        return wrapper
    return decorator

def track_db_query(query_name: str, shard: str = 'main') -> Callable:
    """Декоратор для отслеживания времени выполнения запросов к БД"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                DB_QUERY_LATENCY.labels(
                    query_type=query_name,
                    shard=shard
                ).observe(duration)
                logger.info(f"DB query {query_name} completed in {duration:.3f}s")
                return result
            except Exception as e:
                ERROR_COUNTER.labels(
                    error_type=f"db_{type(e).__name__}",
                    shard=shard
                ).inc()
                raise
        return wrapper
    return decorator

def track_api_errors(api_name: str) -> Callable:
    """Декоратор для отслеживания ошибок в API запросах"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                API_ERRORS.labels(
                    api=api_name,
                    error_type=type(e).__name__
                ).inc()
                raise
        return wrapper
    return decorator
