import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner
from database.database import get_db
from database.queries import get_all_crypto_rates, get_dollar_rate, get_user
from keyboards.inline import back_to_menu_button, get_rates_keyboard
from datetime import datetime
from config import CRYPTO_NAMES

logger = logging.getLogger(__name__)

rates_router = Router()


@rates_router.callback_query(F.data.startswith("toggle_currency_display_"))
async def toggle_currency_display(callback: CallbackQuery, i18n: TranslatorRunner):
    """Переключает отображение валют между рублями и долларами."""
    show_in_rub = callback.data.endswith("rub")
    await show_all_rates(callback, i18n, show_in_rub)


@rates_router.callback_query(F.data == "show_all_currency")
async def show_all_rates(callback: CallbackQuery, i18n: TranslatorRunner, show_in_rub: bool = True):
    """Показывает все курсы криптовалют."""
    try:
        async with get_db() as session:
            user = await get_user(session, callback.from_user.id)
            # Для не русских пользователей всегда показываем в USD
            if user.language != "ru":
                show_in_rub = False
            
            crypto_rates = await get_all_crypto_rates(session)
            dollar_rate = await get_dollar_rate(session)
            
            messages = [i18n.get("rates-header"), ""]
            
            # Показываем курс доллара только для русских пользователей
            if user.language == "ru":
                messages.extend([
                    i18n.get("dollar-rate", price=f"{float(dollar_rate.price):,.2f}"),
                    ""  # Пустая строка для разделения
                ])
            
            for rate in crypto_rates:
                crypto_name = CRYPTO_NAMES.get(rate.currency, rate.currency)
                
                if show_in_rub and dollar_rate:
                    price_rub = float(rate.price) * float(dollar_rate.price)
                    messages.append(i18n.get("rate-format-rub",
                                           name=crypto_name,
                                           symbol=rate.currency,
                                           price=f"{price_rub:,.2f}"))
                else:
                    messages.append(i18n.get("rate-format-usd",
                                           name=crypto_name,
                                           symbol=rate.currency,
                                           price=f"{float(rate.price):,.2f}"))
            
            last_update = max([r.updated_at for r in crypto_rates], default=datetime.utcnow())
            messages.append("")
            messages.append(i18n.get("rates-updated",
                                   time=last_update.strftime("%Y-%m-%d %H:%M:%S")))
            
            # Создаем клавиатуру с кнопкой переключения только для русских пользователей
            keyboard = get_rates_keyboard(i18n, show_in_rub) if user.language == "ru" else back_to_menu_button(i18n)
            
            await callback.message.edit_text(
                "\n".join(messages),
                reply_markup=keyboard
            )
            
    except Exception as e:
        logger.error(f"Error showing rates to user {callback.from_user.id}: {e}")
        await callback.message.edit_text(
            i18n.get("rates-error"),
            reply_markup=back_to_menu_button(i18n)
        )