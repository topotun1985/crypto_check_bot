from aiogram.types import Message, CallbackQuery
from database.database import get_db
from database.models import User
from sqlalchemy import select
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

async def get_or_create_user(message: Message = None, callback: CallbackQuery = None) -> User:
    """Получает или создает пользователя в базе данных"""
    if message:
        telegram_id = message.from_user.id
        username = message.from_user.username
        language_code = message.from_user.language_code
    elif callback:
        telegram_id = callback.from_user.id
        username = callback.from_user.username
        language_code = callback.from_user.language_code
    else:
        raise ValueError("Either message or callback must be provided")

    try:
        from database.queries import add_user, get_user
        
        async with get_db() as session:
            # Ищем пользователя
            user = await get_user(session, telegram_id)

            if not user:
                # Определяем язык
                if language_code:
                    lang = language_code.lower()[:2]
                    if lang in ['de', 'en', 'es', 'fr', 'it', 'pt', 'ru']:
                        language_code = lang
                    else:
                        language_code = 'en'
                else:
                    language_code = 'en'
                
                # Создаем нового пользователя через add_user
                await add_user(session, telegram_id, username, language_code)
                user = await get_user(session, telegram_id)
                logger.info(f"Created new user: {telegram_id} with language: {language_code}")
            
            return user
    except Exception as e:
        logger.error(f"Error in get_or_create_user: {e}")
        raise
