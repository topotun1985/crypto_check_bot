import json
import asyncio
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout, ErrNoServers
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from fluentogram import TranslatorHub
from keyboards.inline import get_new_alert_keyboard
from utils.format_helpers import format_crypto_price

logger = logging.getLogger(__name__)

class GlobalRateLimiter:
    """Глобальный ограничитель для всех сообщений бота"""
    def __init__(self, messages_per_second: int = 100):
        self.messages_per_second = messages_per_second
        self.message_timestamps = []
        self.lock = asyncio.Lock()

    async def can_send(self) -> bool:
        """Проверяет, можно ли отправить сообщение"""
        async with self.lock:
            now = datetime.now()
            # Удаляем старые метки времени
            self.message_timestamps = [
                ts for ts in self.message_timestamps 
                if now - ts < timedelta(seconds=1)
            ]
            
            if len(self.message_timestamps) >= self.messages_per_second:
                return False
                
            self.message_timestamps.append(now)
            return True

    async def wait_for_slot(self):
        """Ожидает, пока не появится возможность отправить сообщение"""
        while not await self.can_send():
            await asyncio.sleep(0.1)

class NotificationService:
    def __init__(self, bot: Bot, translator_hub: TranslatorHub, nats_url: str = "nats://nats:4222"):
        self.bot = bot
        self.translator_hub = translator_hub
        self.nats = NATS()
        self.nats_url = nats_url
        self.user_rate_limit = 5  # сообщений в секунду для одного пользователя
        self._last_sent: Dict[int, datetime] = {}
        self.global_limiter = GlobalRateLimiter(100)  # глобальный лимит 25 сообщений/сек
        
    async def connect(self):
        """Подключение к NATS"""
        try:
            await self.nats.connect(
                self.nats_url,
                reconnect_time_wait=1,
                max_reconnect_attempts=-1,  # бесконечные попытки
                connect_timeout=20
            )
            logger.info("Connected to NATS")
            
            # Инициализируем JetStream
            self.js = self.nats.jetstream()
            
            # Создаем стрим для уведомлений, если его еще нет
            try:
                await self.js.add_stream(name="ALERTS", subjects=["alerts.*"])
            except Exception as e:
                if not "stream name already in use" in str(e).lower():
                    raise
            
            # Подписываемся на очередь уведомлений
            await self.js.subscribe(
                "alerts.notifications",
                durable="notification_processors",
                queue="notification_processors",
                cb=self._notification_handler
            )
            
            # Подписываемся на очередь отложенных уведомлений
            await self.js.subscribe(
                "alerts.delayed",
                durable="delayed_processors",
                queue="delayed_processors",
                cb=self._delayed_notification_handler
            )
            
            logger.info("Subscribed to notification queues")
            
        except ErrNoServers as e:
            logger.error(f"Could not connect to NATS: {e}")
            raise

    async def publish_alert_notification(self, 
                                    user_id: int, 
                                    currency: str,
                                    current_price: float,
                                    threshold: float,
                                    currency_type: str,
                                    condition_type: str,
                                    alert_id: int,
                                    currency_id: int,
                                    user_language: str = "ru",
                                    priority: str = "normal"):
        """Публикация уведомления об алерте в NATS"""
        try:
            i18n = self.translator_hub.get_translator_by_locale(user_language)
            direction = i18n.get("alert-price-above") if condition_type == 'above' else i18n.get("alert-price-below")
            
            message = (
                f"🔔 {currency}\n" +
                i18n.get("alert-price") + f" {direction} {format_crypto_price(threshold)} {currency_type}\n" +
                i18n.get("alerts-current-price") + f" {format_crypto_price(current_price)} {currency_type}"
            )
            
            keyboard = get_new_alert_keyboard(i18n, alert_id, currency_id)
            
            # Преобразуем клавиатуру в словарь для сериализации
            keyboard_dict = {
                "inline_keyboard": [
                    [
                        {
                            "text": button.text,
                            "callback_data": button.callback_data
                        } for button in row
                    ] for row in keyboard.inline_keyboard
                ]
            }
            
            payload = {
                "user_id": user_id,
                "message": message,
                "keyboard": keyboard_dict,
                "priority": priority,
                "timestamp": datetime.utcnow().isoformat(),
                "retry_count": 0
            }
            
            subject = "alerts.notifications" if priority == "high" else "alerts.delayed"
            await self.js.publish(
                subject,
                json.dumps(payload).encode()
            )
        except Exception as e:
            logger.error(f"Error publishing alert notification: {e}")
            raise

    async def _can_send_to_user(self, user_id: int) -> bool:
        """Проверка rate limit для пользователя"""
        now = datetime.now()
        last_sent = self._last_sent.get(user_id)
        if last_sent and (now - last_sent) < timedelta(seconds=1):
            return False
        self._last_sent[user_id] = now
        return True

    async def _notification_handler(self, msg):
        """Обработчик уведомлений из NATS"""
        try:
            data = json.loads(msg.data.decode())
            user_id = data["user_id"]
            message = data["message"]
            keyboard = data.get("keyboard")
            retry_count = data.get("retry_count", 0)
            
            # Проверяем глобальный rate limit
            await self.global_limiter.wait_for_slot()
            
            # Проверяем rate limit пользователя
            if not await self._can_send_to_user(user_id):
                if retry_count < 3:  # максимум 3 попытки
                    # Откладываем отправку
                    await asyncio.sleep(1)
                    data["retry_count"] = retry_count + 1
                    await self.nats.publish(
                        "alerts.delayed",
                        json.dumps(data).encode()
                    )
                return
            
            # Отправляем сообщение
            try:
                if keyboard:
                    # Создаем InlineKeyboardMarkup из словаря
                    keyboard_markup = InlineKeyboardMarkup.model_validate(keyboard)
                    await self.bot.send_message(
                        user_id,
                        message,
                        reply_markup=keyboard_markup
                    )
                else:
                    await self.bot.send_message(user_id, message)
                    
                await msg.ack()  # Подтверждаем успешную обработку
                logger.info(f"Successfully sent notification to user {user_id}")
                
            except Exception as e:
                logger.error(f"Error sending message to user {user_id}: {e}")
                if retry_count < 3:  # максимум 3 попытки
                    data["retry_count"] = retry_count + 1
                    await self.nats.publish(
                        "alerts.delayed",
                        json.dumps(data).encode()
                    )

        except Exception as e:
            logger.error(f"Error processing notification: {e}")

    async def _delayed_notification_handler(self, msg):
        """Обработчик отложенных уведомлений"""
        try:
            data = json.loads(msg.data.decode())
            await asyncio.sleep(1)  # Ждем 1 секунду перед повторной попыткой
            await self.nats.publish(
                "alerts.notifications",
                json.dumps(data).encode()
            )
            await msg.ack()
        except Exception as e:
            logger.error(f"Error processing delayed notification: {e}")

    async def close(self):
        """Закрытие соединения с NATS"""
        try:
            await self.nats.drain()
            await self.nats.close()
        except Exception as e:
            logger.error(f"Error closing NATS connection: {e}")
