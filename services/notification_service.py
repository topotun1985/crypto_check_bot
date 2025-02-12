import json
import asyncio
import logging
from typing import Dict, Optional
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

class GlobalRateLimiter:
    """Глобальный ограничитель для всех сообщений бота"""
    def __init__(self, messages_per_second: int = 30):
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
        self.user_rate_limit = 1  # сообщений в секунду для одного пользователя
        self._last_sent: Dict[int, datetime] = {}
        self.global_limiter = GlobalRateLimiter()

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
            
            # Публикуем в NATS
            json_data = json.dumps(data)
            logger.info(f"Publishing notification with data: {json_data}")
            
            await self.nats.publish(
                "alerts",  # всегда используем основную очередь
                json_data.encode()
            )
            
            logger.info(f"Published alert notification for user {user_id} to alerts queue")
            
        except Exception as e:
            logger.error(f"Error publishing notification: {e}")
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
            
            # Получаем чат для регистрации сообщения
            chat = await self.bot.get_chat(user_id)
            
            # Получаем список активных сообщений для этого чата
            from utils.dialog_manager import _get_chat_messages
            active_messages = _get_chat_messages(chat.id)
            
            # Деактивируем все активные сообщения
            messages_to_deactivate = active_messages.copy()
            for msg_id in messages_to_deactivate:
                try:
                    await self.bot.edit_message_reply_markup(
                        chat_id=chat.id,
                        message_id=msg_id,
                        reply_markup=None
                    )
                    active_messages.remove(msg_id)
                    logger.info(f"Successfully removed keyboard from message {msg_id}")
                except Exception as e:
                    if "message to edit not found" in str(e).lower() or "message is not modified" in str(e).lower():
                        active_messages.remove(msg_id)
                        logger.info(f"Message {msg_id} was already removed or not found")
                    else:
                        logger.warning(f"Failed to remove keyboard from message {msg_id}: {e}")
            
            # Отправляем новое сообщение
            logger.info(f"Preparing to send message. Keyboard data: {keyboard}")
            
            try:
                if keyboard:
                    # Создаем InlineKeyboardMarkup из словаря
                    keyboard_markup = InlineKeyboardMarkup(**keyboard)
                    sent_message = await self.bot.send_message(
                        user_id,
                        message,
                        reply_markup=keyboard_markup
                    )
                    # Регистрируем сообщение с клавиатурой
                    register_message(chat.id, sent_message.message_id)
                    logger.info(f"Sent message with keyboard to user {user_id}")
                else:
                    sent_message = await self.bot.send_message(user_id, message)
                    logger.info(f"Sent message without keyboard to user {user_id}")
                
                logger.info(f"Successfully sent notification to user {user_id}")
                
            except Exception as e:
                logger.error(f"Error sending message: {e}. Keyboard data: {keyboard}")
                if retry_count < 3:  # максимум 3 попытки
                    data["retry_count"] = retry_count + 1
                    await self.nats.publish(
                        "alerts.delayed",
                        json.dumps(data).encode()
                    )
                raise
            
        except Exception as e:
            logger.error(f"Error sending message to user {user_id if 'user_id' in locals() else 'unknown'}: {e}")

    async def _delayed_notification_handler(self, msg):
        """Обработчик отложенных уведомлений"""
        await self._notification_handler(msg)

    async def close(self):
        """Закрытие соединения с NATS"""
        try:
            await self.nats.close()
            logger.info("NATS connection closed")
        except Exception as e:
            logger.error(f"Error closing NATS connection: {e}")
