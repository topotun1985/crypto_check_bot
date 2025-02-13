import logging
from typing import Dict, Set
from aiogram import types, Bot
from aiogram.exceptions import TelegramBadRequest

logger = logging.getLogger(__name__)

# Сохраняем ID сообщений с клавиатурой для каждого чата
_active_messages: Dict[int, Set[int]] = {}

def _get_chat_messages(chat_id: int) -> Set[int]:
    """Получаем список активных сообщений для чата"""
    if chat_id not in _active_messages:
        _active_messages[chat_id] = set()
    return _active_messages[chat_id]

def register_message(chat_id: int, message_id: int):
    """Регистрируем новое сообщение с клавиатурой"""
    messages = _get_chat_messages(chat_id)
    messages.add(message_id)
    logger.info(f"Registered new message {message_id} for chat {chat_id}")

async def deactivate_previous_dialogs(message: types.Message | int, bot: Bot | None = None, keep_message_id: int | None = None):
    """
    Деактивирует предыдущие диалоги пользователя, удаляя клавиатуру.
    
    Args:
        message: Текущее сообщение или chat_id
        bot: Объект бота (необходим, если передан chat_id)
        keep_message_id: ID сообщения, которое нужно оставить (опционально)
    """
    try:
        # Определяем chat_id и bot
        if isinstance(message, types.Message):
            chat_id = message.chat.id
            bot = message.bot
        else:
            chat_id = message
            if bot is None:
                raise ValueError("Bot object is required when using chat_id")

        messages = _get_chat_messages(chat_id)
        messages_to_deactivate = messages.copy()
        
        # Удаляем клавиатуры у старых сообщений
        for msg_id in messages_to_deactivate:
            if keep_message_id and msg_id == keep_message_id:
                continue
                
            try:
                await bot.edit_message_reply_markup(
                    chat_id=chat_id,
                    message_id=msg_id,
                    reply_markup=None
                )
                messages.remove(msg_id)
                logger.info(f"Successfully removed keyboard from message {msg_id}")
            except TelegramBadRequest as e:
                error_text = str(e).lower()
                if "message is not modified" in error_text or "message to edit not found" in error_text:
                    messages.remove(msg_id)
                    logger.info(f"Message {msg_id} was already removed or not found")
                else:
                    logger.warning(f"Failed to remove keyboard from message {msg_id}: {e}")
            except Exception as e:
                # Если ошибка связана с отсутствием сообщения или клавиатуры, просто удаляем его из списка
                if "'NoneType' object has no attribute" in str(e):
                    messages.remove(msg_id)
                    logger.info(f"Message {msg_id} was already removed or not found")
                else:
                    logger.error(f"Unexpected error removing keyboard from message {msg_id}: {e}")
                
    except Exception as e:
        logger.error(f"Error in deactivate_previous_dialogs: {e}")
