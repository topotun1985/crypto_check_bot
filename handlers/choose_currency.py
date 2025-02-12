import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner
from database.database import get_db
from config import CRYPTO_NAMES
from database.queries import (
    get_user_currencies,
    add_user_currency,
    remove_user_currency,
    get_user_subscription,
    SUBSCRIPTION_LIMITS
)
from keyboards.inline import get_choose_currency_keyboard, back_to_menu_button
from utils.dialog_manager import register_message

choose_currency_router = Router()
logger = logging.getLogger(__name__)

@choose_currency_router.callback_query(F.data == "choose_currency")
async def show_currency_selection(callback: CallbackQuery, i18n: TranslatorRunner):
    """Показывает список доступных валют для выбора."""
    try:
        async with get_db() as session:
            user_currencies = await get_user_currencies(session, callback.from_user.id)
            subscription = await get_user_subscription(session, callback.from_user.id)
            currency_limit = SUBSCRIPTION_LIMITS.get(subscription.plan if subscription else "free", SUBSCRIPTION_LIMITS["free"])
            
            message = i18n.get("subscription-currencies", 
                           current=len(user_currencies),
                           max=currency_limit)
            message += "\n\n" + i18n.get("choose-currency-instruction")
            
            await callback.message.edit_text(
                message,
                reply_markup=get_choose_currency_keyboard(i18n, [c.currency for c in user_currencies])
            )
            register_message(callback.message.chat.id, callback.message.message_id)
            
    except Exception as e:
        logger.error(f"Error showing currency selection to user {callback.from_user.id}: {str(e)}")
        await callback.message.edit_text(
            i18n.get("rates-error"),
            reply_markup=back_to_menu_button(i18n)
        )

@choose_currency_router.callback_query(F.data.startswith("toggle_crypto_"))
async def toggle_crypto(callback: CallbackQuery, i18n: TranslatorRunner):
    """Добавляет или удаляет валюту из списка отслеживаемых."""
    try:
        # Деактивируем предыдущие диалоги
        
        crypto = callback.data.split("_")[2]
        async with get_db() as session:
            user_currencies = await get_user_currencies(session, callback.from_user.id)
            is_tracked = any(c.currency == crypto for c in user_currencies)
            
            if is_tracked:
                # Удаляем валюту
                await remove_user_currency(session, callback.from_user.id, crypto)
                await callback.answer(i18n.get("currency-removed", currency=CRYPTO_NAMES[crypto]))
            else:
                try:
                    # Добавляем валюту
                    await add_user_currency(session, callback.from_user.id, crypto)
                    await callback.answer(i18n.get("currency-added", currency=CRYPTO_NAMES[crypto]))
                except ValueError:
                    # Если превышен лимит
                    await callback.answer(i18n.get("subscription-limit-reached"), show_alert=True)
                    return
            
            # Обновляем отображение
            await show_currency_selection(callback, i18n)
            
    except Exception as e:
        logger.error(f"Error toggling crypto for user {callback.from_user.id}: {str(e)}")
        await callback.message.edit_text(
            i18n.get("rates-error"),
            reply_markup=back_to_menu_button(i18n)
        )