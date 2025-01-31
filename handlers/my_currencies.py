import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner
from database.database import get_db
from config import CRYPTO_NAMES, AVAILABLE_CRYPTOCURRENCIES 
from database.queries import (
    get_user_currencies,
    add_user_currency,
    remove_user_currency,
    get_all_crypto_rates,
    get_dollar_rate,
    get_user_subscription,
    SUBSCRIPTION_LIMITS
)
from keyboards.inline import get_my_currencies_keyboard, back_to_menu_button


my_currencies_router = Router()
logger = logging.getLogger(__name__)

async def format_currency_rate(rate, dollar_rate, show_in_rub: bool, i18n: TranslatorRunner) -> str:
    """Форматирует строку с курсом валюты."""
    crypto_name = CRYPTO_NAMES.get(rate.currency, rate.currency)
    
    if show_in_rub and dollar_rate:
        price_rub = float(rate.price) * float(dollar_rate.price)
        return i18n.get("rate-format-rub",
                       name=crypto_name,
                       symbol=rate.currency,
                       price=f"{price_rub:,.2f}")
    else:
        return i18n.get("rate-format-usd",
                       name=crypto_name,
                       symbol=rate.currency,
                       price=f"{float(rate.price):,.2f}")

@my_currencies_router.callback_query(F.data == "show_my_currencies")
async def show_my_currencies(callback: CallbackQuery, i18n: TranslatorRunner, show_in_rub: bool = True):
    """Показывает список валют пользователя."""
    try:
        async with get_db() as session:
            # Получаем валюты пользователя
            user_currencies = await get_user_currencies(session, callback.from_user.id)
            subscription = await get_user_subscription(session, callback.from_user.id)
            currency_limit = SUBSCRIPTION_LIMITS.get(subscription.plan if subscription else "free", SUBSCRIPTION_LIMITS["free"])
            
            # Добавляем информацию о количестве выбранных валют
            header = i18n.get("subscription-currencies", 
                            current=len(user_currencies),
                            max=currency_limit)
            
            if not user_currencies:
                await callback.message.edit_text(
                    i18n.get("my-currencies-empty"),
                    reply_markup=back_to_menu_button(i18n)
                )
                return
            
            # Получаем курсы только для валют пользователя
            crypto_rates = await get_all_crypto_rates(session)
            dollar_rate = await get_dollar_rate(session)
            
            # Формируем сообщение
            messages = [header, ""]
            
            # Создаем словарь курсов для быстрого доступа
            rates_dict = {rate.currency: rate for rate in crypto_rates}
            
            # Перебираем валюты пользователя в порядке их добавления
            for user_currency in user_currencies:
                if rate := rates_dict.get(user_currency.currency):
                    messages.append(await format_currency_rate(rate, dollar_rate, show_in_rub, i18n))
            
            # Добавляем время последнего обновления
            user_rates = [rates_dict[uc.currency] for uc in user_currencies if uc.currency in rates_dict]
            if user_rates:
                last_update = max([r.updated_at for r in user_rates])
                messages.extend([
                    "",  # Пустая строка для разделения
                    i18n.get("rates-updated", time=last_update.strftime("%Y-%m-%d %H:%M:%S"))
                ])
            
            await callback.message.edit_text(
                "\n".join(messages),
                reply_markup=get_my_currencies_keyboard(i18n, show_in_rub)
            )
            
    except Exception as e:
        logger.error(f"Error showing user currencies to user {callback.from_user.id}: {e}")
        await callback.message.edit_text(
            i18n.get("rates-error"),
            reply_markup=back_to_menu_button(i18n)
        )

@my_currencies_router.callback_query(F.data.startswith("toggle_my_currency_display_"))
async def toggle_my_currency_display(callback: CallbackQuery, i18n: TranslatorRunner):
    """Переключает отображение валют между рублями и долларами в разделе 'Мои валюты'."""
    show_in_rub = callback.data.endswith("rub")
    await show_my_currencies(callback, i18n, show_in_rub)

@my_currencies_router.callback_query(F.data.startswith("toggle_currency_display_"))
async def toggle_currency_display(callback: CallbackQuery, i18n: TranslatorRunner):
    """Переключает отображение валют между рублями и долларами."""
    show_in_rub = callback.data.endswith("rub")
    await show_my_currencies(callback, i18n, show_in_rub)