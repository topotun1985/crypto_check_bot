import json
import asyncio
import logging
from typing import Dict, Optional, Set
from datetime import datetime, timedelta
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout, ErrNoServers
from aiogram import Bot, types
from aiogram.types import InlineKeyboardMarkup, Message
from fluentogram import TranslatorHub
from keyboards.inline import get_new_alert_keyboard
from utils.format_helpers import format_crypto_price
from utils.dialog_manager import deactivate_previous_dialogs, register_message

logger = logging.getLogger(__name__)

from .rate_limiter import TelegramRateLimiter

class NotificationService:
    def __init__(self, bot: Bot, translator_hub: TranslatorHub, nats_url: str = "nats://nats:4222"):
        self.bot = bot
        self.translator_hub = translator_hub
        self.nats = NATS()
        self.nats_url = nats_url
        self.rate_limiter = TelegramRateLimiter()
        self._processing_users: Set[int] = set()
        self._processing_lock = asyncio.Lock()

    async def connect(self):
        """Подключение к NATS"""
        try:
            await self.nats.connect(
                self.nats_url,
                reconnect_time_wait=1,
                max_reconnect_attempts=60,
                connect_timeout=20
            )
            
            # Подписываемся на основную очередь уведомлений
            await self.nats.subscribe(
                "alerts",
                cb=self._notification_handler
            )
            
            # Подписываемся на очередь высокоприоритетных уведомлений
            await self.nats.subscribe(
                "alerts.high",
                cb=self._notification_handler
            )
            
            # Подписываемся на очередь отложенных уведомлений
            await self.nats.subscribe(
                "alerts.delayed",
                cb=self._delayed_notification_handler
            )
            
            logger.info("Successfully connected to NATS")
            
        except ErrNoServers as e:
            logger.error(f"Could not connect to NATS: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error connecting to NATS: {e}")
            raise

    async def publish_alert_notification(
        self, 
        user_id: int, 
        currency: str,
        current_price: float,
        threshold: float,
        currency_type: str,
        condition_type: str,
        alert_id: int,
        currency_id: int,
        user_language: str = "ru",
        priority: str = "normal"
    ):
        """Публикация уведомления об алерте в NATS"""
        try:
            # Получаем переводчик для языка пользователя
            i18n = self.translator_hub.get_translator_by_locale(user_language)
            
            # Формируем сообщение
            currency_symbol = 'RUB' if currency_type.upper() == 'RUB' else 'USD'
            direction = i18n.get("alert-price-above") if condition_type == 'above' else i18n.get("alert-price-below")
            message = (
                f"🔔 {currency}\n"+
                i18n.get("alert-price")+f" {direction} {format_crypto_price(threshold)} {currency_symbol}\n"+
                i18n.get("alerts-current-price")+f" {format_crypto_price(current_price)} {currency_symbol}"
            )
            
            # Создаем клавиатуру
            keyboard = get_new_alert_keyboard(i18n, alert_id, currency_id)
            
            # Преобразуем клавиатуру в словарь для JSON сериализации
            keyboard_dict = keyboard.model_dump() if keyboard else None
            
            # Формируем данные для отправки
            data = {
                "user_id": user_id,
                "message": message,
                "keyboard": keyboard_dict,
                "retry_count": 0
            }
            
            # Устанавливаем высокий приоритет для всех уведомлений об алертах
            data['priority'] = 'high'
            
            # Публикуем в NATS
            json_data = json.dumps(data)
            logger.info(f"Publishing notification with data: {json_data}")
            
            await self.nats.publish(
                "alerts.high",  # используем очередь с высоким приоритетом
                json_data.encode()
            )
            
            logger.info(f"Published alert notification for user {user_id} to alerts queue")
            
        except Exception as e:
            logger.error(f"Error publishing notification: {e}")
            raise

    async def _can_send_to_user(self, user_id: int, priority: bool = False) -> bool:
        """Проверка rate limit для пользователя"""
        return await self.rate_limiter.can_send(user_id, priority)

    async def _notification_handler(self, msg):
        """Обработчик уведомлений из NATS"""
        user_id = None
        try:
            # Декодируем сообщение
            data = json.loads(msg.data.decode())
            user_id = data["user_id"]
            message = data["message"]
            keyboard = data.get("keyboard")
            retry_count = data.get("retry_count", 0)
            priority = data.get("priority", "normal")
            is_priority = priority == "high"

            # Проверяем блокировку
            async with self._processing_lock:
                if user_id in self._processing_users:
                    # Пользователь уже обрабатывается
                    if retry_count < 3:
                        await asyncio.sleep(2)
                        data["retry_count"] = retry_count + 1
                        await self.nats.publish(
                            "alerts.delayed",
                            json.dumps(data).encode()
                        )
                    return
                # Блокируем пользователя
                self._processing_users.add(user_id)

            try:
                # Дожидаемся возможности отправить сообщение с учетом rate limit
                can_send = await self.rate_limiter.wait_for_slot(user_id, is_priority)
                if not can_send:
                    # Если не можем отправить сейчас, добавляем в отложенные
                    if retry_count < 3:
                        await asyncio.sleep(1)
                        data["retry_count"] = retry_count + 1
                        await self.nats.publish(
                            "alerts.delayed",
                            json.dumps(data).encode()
                        )
                    return

                # Деактивируем предыдущие диалоги перед отправкой нового
                await deactivate_previous_dialogs(user_id, self.bot)
                
                # Отправляем сообщение
                sent_message = await self.bot.send_message(
                    chat_id=user_id,
                    text=message,
                    reply_markup=keyboard if keyboard else None
                )
                register_message(user_id, sent_message.message_id)
                logger.info(f"Successfully sent notification {sent_message.message_id} to user {user_id}")

            except Exception as e:
                logger.error(f"Error sending notification to user {user_id}: {str(e)}")
                if retry_count < 3:
                    await asyncio.sleep(2)
                    data["retry_count"] = retry_count + 1
                    await self.nats.publish(
                        "alerts.delayed",
                        json.dumps(data).encode()
                    )

            finally:
                # Разблокируем пользователя
                async with self._processing_lock:
                    self._processing_users.remove(user_id)

        except Exception as e:
            logger.error(f"Critical error processing notification: {str(e)}")
            logger.error(f"Stacktrace: {traceback.format_exc()}")

    async def _delayed_notification_handler(self, msg):
        """Обработчик отложенных уведомлений"""
        await asyncio.sleep(5)  # Ждем 5 секунд перед повторной обработкой
        await self._notification_handler(msg)

    async def close(self):
        """Закрытие соединения с NATS"""
        try:
            await self.nats.close()
        except Exception as e:
            logger.error(f"Error closing NATS connection: {e}")
            raise
