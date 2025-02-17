import asyncio
from aiogram import Bot
from prometheus_client import start_http_server
from .prometheus_metrics import (
    ACTIVE_USERS, TOTAL_USERS, PREMIUM_USERS,
    REQUEST_LATENCY, DB_QUERY_LATENCY,
    ERROR_COUNTER, API_ERRORS,
    MEMORY_USAGE, CPU_USAGE, DB_CONNECTIONS
)
from .telegram_alerts import TelegramAlerter
from config import TELEGRAM_ALERTS_CHANNEL_ID, TELEGRAM_ADMIN_ID
import logging

logger = logging.getLogger(__name__)

class MonitoringService:
    def __init__(
        self,
        bot: Bot,
        prometheus_port: int = None,
        alerter_port: int = 9087,
        channel_id: str = "-1002266901682",
        admin_id: int = 855277058
    ):
        import os
        self.bot = bot
        self.prometheus_port = int(os.getenv('PROMETHEUS_PORT', prometheus_port or 9091))
        self.alerter_port = alerter_port
        self.channel_id = TELEGRAM_ALERTS_CHANNEL_ID
        self.admin_id = TELEGRAM_ADMIN_ID
        self.alerter = None


    async def start(self):
        """Запускает все сервисы мониторинга"""
        try:
            # Запускаем Prometheus метрики
            start_http_server(port=self.prometheus_port, addr='0.0.0.0')
            logger.info(f"Started Prometheus metrics server on 0.0.0.0:{self.prometheus_port}")

            # Инициализируем и запускаем TelegramAlerter
            self.alerter = TelegramAlerter(
                bot=self.bot,
                channel_id=self.channel_id,
                admin_id=self.admin_id
            )
            logger.info(f"Starting Telegram alerter on port {self.alerter_port}")
            await self.alerter.start(port=self.alerter_port)
            logger.info(f"Started Telegram alerter successfully")

            # Запускаем фоновые задачи обновления метрик
            asyncio.create_task(self._update_metrics())
            logger.info("Started background metrics update task")

        except Exception as e:
            logger.error(f"Failed to start monitoring services: {e}")
            raise

    async def _update_metrics(self):
        """Периодически обновляет метрики"""
        import psutil
        import os
        from datetime import datetime, timedelta
        from database.database import get_db, session_factory
        from database.models import User, Subscription
        from sqlalchemy import func, and_, select, text

        while True:
            try:
                # Обновляем метрики каждые 15 секунд
                await asyncio.sleep(15)

                # Обновляем метрики использования ресурсов
                process = psutil.Process(os.getpid())
                MEMORY_USAGE.labels(shard="main").set(process.memory_info().rss)
                # Измеряем CPU за последнюю секунду
                CPU_USAGE.labels(shard="main").set(psutil.cpu_percent(interval=1))

                # Обновляем метрики пользователей и БД
                from .decorators import track_db_query

                @track_db_query('get_connections', 'main')
                async def get_db_connections(session):
                    result = await session.execute(text("SELECT count(*) FROM pg_stat_activity"))
                    return result.scalar()

                @track_db_query('get_total_users', 'main')
                async def get_total_users(session):
                    result = await session.execute(select(func.count(User.id)))
                    return result.scalar()

                @track_db_query('get_premium_users', 'main')
                async def get_premium_users(session):
                    query = select(func.count(User.id)).join(Subscription).where(
                        Subscription.expires_at > datetime.utcnow()
                    )
                    result = await session.execute(query)
                    return result.scalar()

                @track_db_query('get_active_users', 'main')
                async def get_active_users(session):
                    query = select(func.count(User.id)).where(
                        User.updated_at > datetime.utcnow() - timedelta(hours=24)
                    )
                    result = await session.execute(query)
                    return result.scalar()

                async with get_db() as session:
                    # Подсчет активных подключений
                    conn_count = await get_db_connections(session)
                    DB_CONNECTIONS.labels(shard='main').set(conn_count or 0)

                    # Подсчет общего количества пользователей
                    total_users = await get_total_users(session)
                    TOTAL_USERS.labels(shard='main').set(total_users or 0)

                    # Подсчет премиум пользователей
                    premium_users = await get_premium_users(session)
                    PREMIUM_USERS.labels(shard='main').set(premium_users or 0)

                    # Подсчет активных пользователей
                    active_users = await get_active_users(session)
                    ACTIVE_USERS.labels(shard='main').set(active_users or 0)
                    ACTIVE_USERS.labels(shard='main').set(active_users or 0)

                    logger.info(f"Updated metrics - Active: {active_users}, Total: {total_users}, Premium: {premium_users}, DB Connections: {conn_count}")

            except Exception as e:
                logger.error(f"Error updating metrics: {e}")
                ERROR_COUNTER.labels(error_type='metrics_update_error', shard='system').inc()

    async def stop(self):
        """Останавливает все сервисы мониторинга"""
        if self.alerter:
            # Здесь добавим логику остановки alerter'а когда она будет реализована
            pass
        logger.info("Monitoring services stopped")
