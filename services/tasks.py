import asyncio
import logging
from config import AVAILABLE_CRYPTOCURRENCIES
from services.binance_api import CryptoService
from services.cmc_api import FiatService
from database.database import get_db
from database.queries import update_crypto_rate, update_dollar_rate, reset_expired_subscriptions

logger = logging.getLogger(__name__)

class BackgroundTasks:
    def __init__(self):
        self.crypto_service = CryptoService()
        self.fiat_service = FiatService()
        self.is_running = False

    async def start(self):
        """Запуск фоновых задач"""
        if not self.is_running:
            self.is_running = True
            asyncio.create_task(self.update_crypto_prices())
            asyncio.create_task(self.update_usd_rate())
            asyncio.create_task(self.check_expired_subscriptions())
            logger.info("Фоновые задачи запущены")

    async def update_crypto_prices(self):
        """Обновление цен криптовалют (раз в минуту)"""
        while self.is_running:
            async with get_db() as session:
                for symbol in AVAILABLE_CRYPTOCURRENCIES:
                    try:
                        price = await self.crypto_service.get_binance_price(symbol)
                        if price is not None:
                            await update_crypto_rate(session, symbol, price)
                            logger.info(f"{symbol}: {price} USDT")
                    except Exception as e:
                        logger.error(f"Ошибка обновления {symbol}: {e}")
            await asyncio.sleep(60)

    async def update_usd_rate(self):
        """Обновление курса USD/RUB (раз в 10 минут)"""
        while self.is_running:
            try:
                async with get_db() as session:
                    rate = await self.fiat_service.get_usd_rate()
                    if rate is not None:
                        await update_dollar_rate(session, rate)
                        logger.info(f"USD/RUB: {rate}")
            except Exception as e:
                logger.error(f"Ошибка обновления USD/RUB: {e}")
            await asyncio.sleep(600)

    async def check_expired_subscriptions(self):
        """Проверяет истекшие подписки и сбрасывает их раз в час"""
        while self.is_running:
            async with get_db() as session:
                try:
                    await reset_expired_subscriptions(session)
                    logger.info("Проверены истекшие подписки")
                except Exception as e:
                    logger.error(f"Ошибка при проверке подписок: {e}")
            await asyncio.sleep(600) # Проверяем раз в час (для теста раз в 10 минут)
            