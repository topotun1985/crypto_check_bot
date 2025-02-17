from functools import wraps
import time
from monitoring.prometheus_metrics import REQUEST_LATENCY, ERROR_COUNTER
import logging

logger = logging.getLogger(__name__)

def track_handler_metrics(handler_name):
    """Декоратор для отслеживания метрик обработчика"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                REQUEST_LATENCY.labels(
                    operation=handler_name,
                    shard='main'
                ).observe(time.time() - start_time)
                return result
            except Exception as e:
                ERROR_COUNTER.labels(
                    error_type=type(e).__name__,
                    shard='main'
                ).inc()
                logger.exception(f"Error in handler {handler_name}: {str(e)}")
                raise
        return wrapper
    return decorator
