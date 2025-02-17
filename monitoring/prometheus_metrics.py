from prometheus_client import Counter, Histogram, Gauge, start_http_server
import psutil
import time
from typing import Optional
from functools import wraps

# Метрики пользователей
ACTIVE_USERS = Gauge('bot_active_users', 'Number of active users', ['shard'])
TOTAL_USERS = Gauge('bot_total_users', 'Total number of registered users', ['shard'])
PREMIUM_USERS = Gauge('bot_premium_users', 'Number of premium users', ['shard'])

# Метрики производительности
REQUEST_LATENCY = Histogram(
    'bot_request_duration_seconds',
    'Request latency in seconds',
    ['operation', 'shard'],
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
)

DB_QUERY_LATENCY = Histogram(
    'bot_db_query_duration_seconds',
    'Database query latency in seconds',
    ['query_type', 'shard'],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0)
)

# Метрики ошибок
ERROR_COUNTER = Counter('bot_errors_total', 'Number of errors', ['error_type', 'shard'])
API_ERRORS = Counter('bot_api_errors_total', 'Number of API errors', ['api_name', 'error_type'])

# Метрики ресурсов
MEMORY_USAGE = Gauge('bot_memory_usage_bytes', 'Memory usage in bytes', ['shard'])
CPU_USAGE = Gauge('bot_cpu_usage_percent', 'CPU usage percentage', ['shard'])
DB_CONNECTIONS = Gauge('bot_db_connections', 'Number of database connections', ['shard'])

# Метрики очередей NATS
QUEUE_SIZE = Gauge('bot_queue_size', 'Number of messages in queue', ['queue_name'])
QUEUE_LAG = Gauge('bot_queue_lag_seconds', 'Message processing lag in seconds', ['queue_name'])
MESSAGE_PROCESSING_TIME = Histogram(
    'bot_message_processing_seconds',
    'Message processing time in seconds',
    ['queue_name'],
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
)

# Метрики бэкапов
BACKUP_STATUS = Gauge('bot_backup_status', 'Status of the last backup (1 = success, 0 = failure)', ['type'])
BACKUP_SIZE = Gauge('bot_backup_size_bytes', 'Size of the last backup in bytes', ['type'])
BACKUP_DURATION = Histogram(
    'bot_backup_duration_seconds',
    'Time taken to complete backup',
    ['type'],
    buckets=(1.0, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0)
)

# Метрики использования диска
DISK_USAGE = Gauge('bot_disk_usage_bytes', 'Disk space usage', ['path', 'type'])
DISK_IO = Counter('bot_disk_io_total', 'Disk I/O operations', ['operation'])

# Бизнес-метрики
ALERTS_SENT = Counter('bot_alerts_sent_total', 'Number of price alerts sent', ['currency', 'alert_type'])
SUBSCRIPTION_OPERATIONS = Counter('bot_subscription_operations_total', 'Number of subscription operations', ['operation_type'])
NEW_SUBSCRIPTIONS = Counter('bot_new_subscriptions_total', 'Number of new subscriptions', ['shard'])

def track_latency(operation: str, shard: str = 'default'):
    """Декоратор для отслеживания времени выполнения операций"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                REQUEST_LATENCY.labels(operation=operation, shard=shard).observe(
                    time.time() - start_time
                )
                return result
            except Exception as e:
                ERROR_COUNTER.labels(error_type=type(e).__name__, shard=shard).inc()
                raise
        return wrapper
    return decorator

def track_db_query(query_type: str, shard: str = 'default'):
    """Декоратор для отслеживания времени выполнения запросов к БД"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                DB_QUERY_LATENCY.labels(query_type=query_type, shard=shard).observe(
                    time.time() - start_time
                )
                return result
            except Exception as e:
                ERROR_COUNTER.labels(error_type=f"db_{type(e).__name__}", shard=shard).inc()
                raise
        return wrapper
    return decorator

async def update_resource_metrics():
    """Обновление метрик использования ресурсов"""
    while True:
        try:
            # Обновление метрик памяти
            memory = psutil.Process().memory_info()
            MEMORY_USAGE.labels(shard='main').set(memory.rss)

            # Обновление метрик CPU
            CPU_USAGE.labels(shard='main').set(psutil.Process().cpu_percent())

            # Обновление метрик диска
            for path in ['/backups', '/var/lib/postgresql/data']:
                try:
                    usage = psutil.disk_usage(path)
                    DISK_USAGE.labels(path=path, type='total').set(usage.total)
                    DISK_USAGE.labels(path=path, type='used').set(usage.used)
                    DISK_USAGE.labels(path=path, type='free').set(usage.free)
                except Exception as disk_error:
                    ERROR_COUNTER.labels(error_type='disk_metric_error', shard='system').inc()

            # Ждем 15 секунд перед следующим обновлением
            await asyncio.sleep(15)
        except Exception as e:
            ERROR_COUNTER.labels(error_type='resource_update_error', shard='system').inc()

def init_prometheus_metrics(port: int = 9090):
    """Инициализация и запуск сервера метрик Prometheus"""
    start_http_server(port)
    asyncio.create_task(update_resource_metrics())
