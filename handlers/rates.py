import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner
from database.database import get_db
from database.queries import get_all_crypto_rates, get_dollar_rate, get_user
from services.redis_cache import RedisCache
from keyboards.inline import back_to_menu_button, get_rates_keyboard
from datetime import datetime
from config import CRYPTO_NAMES
from utils.format_helpers import format_crypto_price
from utils.dialog_manager import register_message

logger = logging.getLogger(__name__)

rates_router = Router()


@rates_router.callback_query(F.data.startswith("toggle_currency_display_"))
async def toggle_currency_display(callback: CallbackQuery, i18n: TranslatorRunner):
    """Переключает отображение валют между рублями и долларами."""
    try:
        show_in_rub = callback.data.endswith("rub")
        await show_all_rates(callback, i18n, show_in_rub)
    except Exception as e:
        logger.error(f"Error in toggle_currency_display for user {callback.from_user.id}: {str(e)}")
        await callback.message.answer(i18n.get('alerts-error'))


@rates_router.callback_query(F.data == "show_all_currency")
async def show_all_rates(callback: CallbackQuery, i18n: TranslatorRunner, show_in_rub: bool = True):
    """Показывает все курсы криптовалют."""
    try:
        redis_cache = RedisCache()
        # Используем telegram_id для определения шарда
        async with get_db(telegram_id=callback.from_user.id) as session:
            user = await get_user(session, callback.from_user.id)
            # Для не русских пользователей всегда показываем в USD
            # Для не русских пользователей всегда показываем в USD
            if user.language != "ru":
                show_in_rub = False
            
            # Пробуем получить курсы из Redis
            crypto_rates = await redis_cache.get_crypto_rates()
            dollar_rate = await redis_cache.get_dollar_rate()
            
            # Если в Redis нет данных, берем из БД
            if not crypto_rates:
                db_rates = await get_all_crypto_rates(session)
                crypto_rates = {rate.currency: float(rate.price) for rate in db_rates}
                
            if not dollar_rate and show_in_rub:
                db_dollar = await get_dollar_rate(session)
                dollar_rate = float(db_dollar.price) if db_dollar else None
            
            messages = [i18n.get("rates-header"), ""]
            
            # Показываем курс доллара только для русских пользователей
            if user.language == "ru" and dollar_rate:
                messages.extend([
                    i18n.get("dollar-rate", price=f"{dollar_rate:,.2f}"),
                    ""  # Пустая строка для разделения
                ])
            
            for currency, price in crypto_rates.items():
                crypto_name = CRYPTO_NAMES.get(currency, currency)
                
                if show_in_rub and dollar_rate:
                    price_rub = float(price) * dollar_rate
                    messages.append(i18n.get("rate-format-rub",
                                           name=crypto_name,
                                           symbol=currency,
                                           price=format_crypto_price(price_rub)))
                else:
                    messages.append(i18n.get("rate-format-usd",
                                           name=crypto_name,
                                           symbol=currency,
                                           price=format_crypto_price(float(price))))
            
            messages.append("")
            messages.append(i18n.get("rates-updated",
                                   time=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))
            
            # Создаем клавиатуру с кнопкой переключения только для русских пользователей
            keyboard = get_rates_keyboard(i18n, show_in_rub, user.language)
            
            await callback.message.edit_text(
                "\n".join(messages),
                reply_markup=keyboard
            )
            register_message(callback.message.chat.id, callback.message.message_id)
            
    except Exception as e:
        logger.error(f"Error showing rates to user {callback.from_user.id}: {str(e)}")
        await callback.message.edit_text(
            i18n.get("rates-error"),
            reply_markup=back_to_menu_button(i18n)
        )
        