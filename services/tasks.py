import asyncio
import logging
from config import AVAILABLE_CRYPTOCURRENCIES
from services.binance_api import CryptoService
from services.cmc_api import FiatService
from services.redis_cache import RedisCache
from database.database import get_db
from database.queries import update_crypto_rate, update_dollar_rate, reset_expired_subscriptions
from handlers.notification_settings import check_alert_conditions

logger = logging.getLogger(__name__)

class BackgroundTasks:
    def __init__(self, bot=None, notification_service=None):
        self.crypto_service = CryptoService()
        self.fiat_service = FiatService()
        self.redis_cache = RedisCache()
        self.is_running = False
        self.bot = bot
        self.i18n = None
        self.notification_service = notification_service
        self.alert_service = None

    async def start(self):
        """Запуск фоновых задач"""
        if not self.is_running:
            self.is_running = True
            asyncio.create_task(self.update_crypto_prices())
            asyncio.create_task(self.update_usd_rate())
            asyncio.create_task(self.check_expired_subscriptions())
            if self.bot:
                asyncio.create_task(self.check_alerts())
            logger.info("Фоновые задачи запущены")

    async def update_crypto_prices(self):
        """Обновление цен криптовалют (раз в минуту)"""
        while self.is_running:
            try:
                # Получаем все курсы за один проход
                rates = {}
                for symbol in AVAILABLE_CRYPTOCURRENCIES:
                    try:
                        if price := await self.crypto_service.get_binance_price(symbol):
                            rates[symbol] = price
                            logger.debug(f"{symbol}: {price} USDT")  # Меняем уровень логирования на debug
                    except Exception as e:
                        logger.error(f"Ошибка получения курса {symbol}: {e}")

                if rates:
                    # Сохраняем в Redis
                    await self.redis_cache.set_crypto_rates(rates)
                    
                    # Сохраняем в БД
                    async with get_db(telegram_id=None) as session:
                        for symbol, price in rates.items():
                            await update_crypto_rate(session, symbol, price)
                        
                        # Алерты проверяются в отдельном методе check_alerts
                            
            except Exception as e:
                logger.error(f"Ошибка при обновлении курсов: {e}")
                
            await asyncio.sleep(60)

    async def update_usd_rate(self):
        """Обновление курса USD/RUB (раз в 10 минут)"""
        while self.is_running:
            try:
                if rate := await self.fiat_service.get_usd_rate():
                    # Сохраняем в Redis
                    await self.redis_cache.set_dollar_rate(rate)
                    
                    # Сохраняем в БД
                    async with get_db(telegram_id=None) as session:
                        await update_dollar_rate(session, rate)
                        logger.info(f"USD/RUB: {rate}")
            except Exception as e:
                logger.error(f"Ошибка обновления USD/RUB: {e}")
            await asyncio.sleep(600)

    async def check_expired_subscriptions(self):
        """Проверяет истекшие подписки и сбрасывает их раз в час"""
        while self.is_running:
            async with get_db(telegram_id=None) as session:
                try:
                    await reset_expired_subscriptions(session)
                    logger.info("Проверены истекшие подписки")
                except Exception as e:
                    logger.error(f"Ошибка при проверке подписок: {e}")
            await asyncio.sleep(600) # Проверяем раз в час (для теста раз в 10 минут)
            
    async def check_alerts(self):
        """Проверяет условия алертов и отправляет уведомления (раз в минуту)"""
        while self.is_running:
            try:
                # Only proceed if we have both i18n and notification service
                if not (self.i18n and self.notification_service):
                    logger.warning("Missing i18n or notification service for alert checking")
                    await asyncio.sleep(60)
                    continue

                # Initialize alert service if needed
                if not self.alert_service:
                    from services.alert_service import AlertService
                    self.alert_service = AlertService(
                        notification_service=self.notification_service,
                        translator_hub=self.i18n._translator_hub
                        )
                    await self.alert_service.start()
                else:
                    if not self.i18n:
                        logger.error("i18n не инициализирован для проверки алертов")
                    if not self.notification_service:
                        logger.error("notification_service не инициализирован для проверки алертов")
                    if not self.shard_manager:
                        logger.error("shard_manager не инициализирован для проверки алертов")
            except Exception as e:
                logger.error(f"Ошибка при проверке алертов: {e}")
            await asyncio.sleep(60)
            