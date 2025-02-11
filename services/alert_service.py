import asyncio
import logging
from typing import Dict, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Alert, UserCurrency, User
from database.sharding import ShardManager
from database.repositories.alert_repository import AlertRepository
from services.redis_cache import RedisCache
from services.notification_service import NotificationService
from fluentogram import TranslatorHub

logger = logging.getLogger(__name__)

class AlertService:
    def __init__(self, 
                 notification_service: NotificationService, 
                 shard_manager: ShardManager,
                 translator_hub: TranslatorHub,
                 check_interval: int = 60):
        self.notification_service = notification_service
        self.shard_manager = shard_manager
        self.translator_hub = translator_hub
        self.redis = RedisCache()
        self.alert_repository = AlertRepository(shard_manager)
        self.check_interval = check_interval
        self._is_running = False
        
    async def start(self):
        """Запускает процесс проверки алертов"""
        self._is_running = True
        while self._is_running:
            try:
                await self.check_alerts()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in alert checker: {e}")
                await asyncio.sleep(5)

    async def stop(self):
        """Останавливает процесс проверки алертов"""
        self._is_running = False
        
    async def check_alerts(self):
        """Проверка алертов по всем шардам"""
        # Получаем курсы из кэша
        rates = await self.redis.get_crypto_rates()
        if not rates:
            logger.warning("No rates available in cache")
            return
            
        # Получаем курс доллара
        dollar_rate = await self.redis.get_dollar_rate()
        if not dollar_rate:
            logger.warning("No dollar rate available in cache")
            return
            
        # Проверяем алерты по шардам параллельно
        tasks = []
        for shard_id in range(self.shard_manager.shard_count):
            task = self._check_shard_alerts(shard_id, rates, dollar_rate)
            tasks.append(asyncio.create_task(task))
            
        await asyncio.gather(*tasks)
        
    async def _check_shard_alerts(self, shard_id: int, rates: Dict[str, float], dollar_rate: float):
        """Проверка алертов для конкретного шарда"""
        async with AsyncSession(self.shard_manager.get_engine(shard_id)) as session:
            try:
                # Получаем активные алерты через репозиторий
                alerts = await self.alert_repository.get_active_alerts_for_shard(shard_id, session)
                
                for alert, user_currency, user in alerts:
                    current_price = rates.get(user_currency.currency)
                    if not current_price:
                        continue

                    # Конвертируем цену в нужную валюту
                    price_in_currency = current_price
                    if alert.currency_type.upper() == 'RUB':
                        price_in_currency *= dollar_rate
                    
                    # Проверяем условие
                    if self._check_alert_condition(alert, price_in_currency):
                        try:
                            # Отправляем уведомление через NATS
                            await self.notification_service.publish_alert_notification(
                                user_id=user.telegram_id,
                                currency=user_currency.currency,
                                current_price=price_in_currency,
                                threshold=float(alert.threshold),
                                currency_type=alert.currency_type.upper(),
                                condition_type=alert.condition_type,
                                alert_id=alert.id,
                                user_language=user.language or "ru",
                                priority="high"
                            )
                            
                            # Обновляем статус алерта
                            await self.alert_repository.update_alert_status(
                                alert=alert,
                                is_active=False,
                                session=session,
                                last_triggered_at=datetime.utcnow()
                            )
                            
                        except Exception as e:
                            logger.error(f"Error processing alert {alert.id}: {e}")
                            continue
                            
                await session.commit()
                
            except Exception as e:
                logger.error(f"Error checking alerts in shard {shard_id}: {e}")
                await session.rollback()

    def _check_alert_condition(self, alert: Alert, current_price: float) -> bool:
        """Проверяет условие алерта"""
        threshold = float(alert.threshold)
        if alert.condition_type == "above":
            return current_price > threshold
        return current_price < threshold
