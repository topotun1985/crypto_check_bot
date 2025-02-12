import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from fluentogram import TranslatorRunner
from database.database import get_db
from database.queries import get_user


logger = logging.getLogger(__name__)


class TranslatorRunnerMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user: User = data.get('event_from_user')

        if user is None:
            return await handler(event, data)

        # hub: TranslatorRunner = data.get('_translator_hub')
        # data['i18n'] = hub.get_translator_by_locale(locale=user.language_code)

        try:
            # Получаем язык из БД
            async with get_db(telegram_id=user.id) as session:
                db_user = await get_user(session, user.id)
                if db_user:
                    locale = db_user.language
                else:
                    locale = user.language_code or 'en'
        except Exception as e:
            logger.error(f"Error getting user language from database: {e}")
            locale = user.language_code or 'en'
    
        hub: TranslatorRunner = data.get('_translator_hub')
        data['i18n'] = hub.get_translator_by_locale(locale=locale)
    

        return await handler(event, data)
        
