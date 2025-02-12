import asyncio
import logging
from typing import Dict, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Alert, UserCurrency, User
from database.database import get_db
from sqlalchemy import select
from services.redis_cache import RedisCache
from services.notification_service import NotificationService
from fluentogram import TranslatorHub

logger = logging.getLogger(__name__)

class AlertService:
    def __init__(self, 
                 notification_service: NotificationService, 
                 translator_hub: TranslatorHub,
                 check_interval: int = 60):
        self.notification_service = notification_service
        self.translator_hub = translator_hub
        self.redis = RedisCache()
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
            
        # Проверяем алерты
        await self._check_alerts(rates, dollar_rate)
        
    async def _check_alerts(self, rates: Dict[str, float], dollar_rate: float):
        """Проверка алертов"""
        try:
            # Use a single database session for all alerts
            async with get_db(telegram_id=None) as session:
                # Получаем активные алерты
                result = await session.execute(
                    select(Alert, UserCurrency, User)
                    .join(UserCurrency, Alert.user_currency_id == UserCurrency.id)
                    .join(User, UserCurrency.user_id == User.id)
                    .where(Alert.is_active == True)
                )
                alerts = result.all()
                
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
                                currency_id=user_currency.id,
                                user_language=user.language or "ru",
                                priority="high"
                            )
                            
                            # Деактивируем алерт после отправки уведомления
                            alert.is_active = False
                            alert.last_triggered_at = datetime.utcnow()
                            alert.updated_at = datetime.utcnow()
                            await session.commit()
                            
                        except Exception as e:
                            logger.error(f"Error processing alert {alert.id}: {e}")
                            continue
                            
                await session.commit()
                
        except Exception as e:
            logger.error(f"Error checking alerts: {e}")
            await session.rollback()

    def _check_alert_condition(self, alert: Alert, current_price: float) -> bool:
        """Проверяет условие алерта"""
        threshold = float(alert.threshold)
        if alert.condition_type == "above":
            return current_price > threshold
        return current_price < threshold
