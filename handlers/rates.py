import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner
from database.database import get_db
from database.queries import get_all_crypto_rates, get_dollar_rate, get_user
from keyboards.inline import back_to_menu_button
from datetime import datetime
from config import CRYPTO_NAMES

logger = logging.getLogger(__name__)

rates_router = Router()

@rates_router.callback_query(F.data == "show_all_currency")
async def show_all_rates(callback: CallbackQuery, i18n: TranslatorRunner):
    """Показывает все курсы криптовалют."""
    try:
        async with get_db() as session:
            # Получаем пользователя для определения языка
            user = await get_user(session, callback.from_user.id)
            show_in_rub = user.language == "ru"
            
            # Получаем курсы
            crypto_rates = await get_all_crypto_rates(session)
            dollar_rate = await get_dollar_rate(session)
            
            # Формируем сообщение
            messages = [i18n.get("rates-header"), ""]  # Добавляем пустую строку для разделения
            
            for rate in crypto_rates:
                # Получаем полное название криптовалюты
                crypto_name = CRYPTO_NAMES.get(rate.currency, rate.currency)
                
                if show_in_rub and dollar_rate:
                    # Конвертируем в рубли
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
            
            # Добавляем время последнего обновления
            last_update = max([r.updated_at for r in crypto_rates], default=datetime.utcnow())
            messages.append("")  # Пустая строка для разделения
            messages.append(i18n.get("rates-updated",
                                   time=last_update.strftime("%Y-%m-%d %H:%M:%S UTC")))
            
            # Отправляем сообщение
            await callback.message.edit_text(
                "\n".join(messages),
                reply_markup=back_to_menu_button(i18n)
            )
            
            logger.info(f"Rates shown to user {callback.from_user.id}")
            
    except Exception as e:
        logger.error(f"Error showing rates to user {callback.from_user.id}: {e}")
        await callback.message.edit_text(
            "❌ Произошла ошибка при получении курсов. Пожалуйста, попробуйте позже.",
            reply_markup=back_to_menu_button(i18n)
        )