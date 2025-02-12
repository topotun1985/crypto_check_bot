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
    elif callback:
        telegram_id = callback.from_user.id
        username = callback.from_user.username
    else:
        raise ValueError("Either message or callback must be provided")

    try:
        # Используем telegram_id для определения шарда
        async with get_db() as session:
            # Ищем пользователя
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()

            if not user:
                # Создаем нового пользователя
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(user)
                await session.commit()
                logger.info(f"Created new user: {telegram_id}")
            
            return user
    except Exception as e:
        logger.error(f"Error in get_or_create_user: {e}")
        raise
