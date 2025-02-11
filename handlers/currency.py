import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner
from database.database import get_db
from database.queries import (
    get_user_currencies,
    add_user_currency,
    remove_user_currency,
    get_user_subscription,
    get_subscription_limit,
    get_user_currency_count
)
from keyboards.inline import (
    get_currency_keyboard,
    get_currency_management_keyboard,
    back_to_menu_button
)
from config import CRYPTO_NAMES

logger = logging.getLogger(__name__)

currency_router = Router()

@currency_router.callback_query(F.data == "manage_currencies")
async def show_currency_menu(callback: CallbackQuery, i18n: TranslatorRunner):
    """Показывает меню управления валютами."""
    try:
        user_id = callback.from_user.id
        async with get_db(user_id=user_id) as session:
            user_currencies = await get_user_currencies(session, user_id)
            subscription = await get_user_subscription(session, user_id)
            
            currency_limit = get_subscription_limit(subscription.plan if subscription else "free")
            currency_count = await get_user_currency_count(session, user_id)
            
            # Формируем список отслеживаемых валют
            tracked_currencies = [uc.currency for uc in user_currencies]
            
            # Формируем текст сообщения
            message_parts = [
                i18n.get("currency-management-header"),
                "",
                i18n.get("subscription-currencies", current=currency_count, max=currency_limit),
                "",
                i18n.get("tracked-currencies-header") if tracked_currencies else i18n.get("no-tracked-currencies")
            ]
            
            if tracked_currencies:
                for currency in tracked_currencies:
                    message_parts.append(f"• {currency}")
            
            await callback.message.edit_text(
                "\n".join(message_parts),
                reply_markup=get_currency_management_keyboard(i18n)
            )

    except Exception as e:
        logger.error(f"Error in show_currency_menu: {e}")
        await callback.message.edit_text(
            i18n.get("error-occurred"),
            reply_markup=back_to_menu_button(i18n)
        )

@currency_router.callback_query(F.data == "add_currency")
async def show_add_currency(callback: CallbackQuery, i18n: TranslatorRunner):
    """Показывает список доступных для добавления валют."""
    try:
        user_id = callback.from_user.id
        async with get_db(user_id=user_id) as session:
            user_currencies = await get_user_currencies(session, user_id)
            tracked_currencies = [uc.currency for uc in user_currencies]
            
            # Получаем список доступных валют (те, которые еще не отслеживаются)
            available_currencies = [c for c in CRYPTO_NAMES if c not in tracked_currencies]
            
            if not available_currencies:
                await callback.message.edit_text(
                    i18n.get("no-currencies-to-add"),
                    reply_markup=get_currency_management_keyboard(i18n)
                )
                return
            
            await callback.message.edit_text(
                i18n.get("select-currency-to-add"),
                reply_markup=get_currency_keyboard(available_currencies, "add", i18n)
            )

    except Exception as e:
        logger.error(f"Error in show_add_currency: {e}")
        await callback.message.edit_text(
            i18n.get("error-occurred"),
            reply_markup=back_to_menu_button(i18n)
        )

@currency_router.callback_query(F.data == "remove_currency")
async def show_remove_currency(callback: CallbackQuery, i18n: TranslatorRunner):
    """Показывает список валют для удаления."""
    try:
        user_id = callback.from_user.id
        async with get_db(user_id=user_id) as session:
            user_currencies = await get_user_currencies(session, user_id)
            
            if not user_currencies:
                await callback.message.edit_text(
                    i18n.get("no-currencies-to-remove"),
                    reply_markup=get_currency_management_keyboard(i18n)
                )
                return
            
            tracked_currencies = [uc.currency for uc in user_currencies]
            await callback.message.edit_text(
                i18n.get("select-currency-to-remove"),
                reply_markup=get_currency_keyboard(tracked_currencies, "remove", i18n)
            )

    except Exception as e:
        logger.error(f"Error in show_remove_currency: {e}")
        await callback.message.edit_text(
            i18n.get("error-occurred"),
            reply_markup=back_to_menu_button(i18n)
        )

@currency_router.callback_query(F.data.startswith("add_"))
async def handle_add_currency(callback: CallbackQuery, i18n: TranslatorRunner):
    """Обрабатывает добавление новой валюты."""
    try:
        currency = callback.data.split("_")[1]
        user_id = callback.from_user.id
        
        async with get_db(user_id=user_id) as session:
            # Проверяем лимит валют для текущего тарифа
            subscription = await get_user_subscription(session, user_id)
            currency_limit = get_subscription_limit(subscription.plan if subscription else "free")
            currency_count = await get_user_currency_count(session, user_id)
            
            if currency_count >= currency_limit:
                await callback.message.edit_text(
                    i18n.get("currency-limit-reached", limit=currency_limit),
                    reply_markup=get_currency_management_keyboard(i18n)
                )
                return
            
            # Добавляем валюту
            await add_user_currency(session, user_id, currency)
            
            await callback.message.edit_text(
                i18n.get("currency-added-successfully", currency=currency),
                reply_markup=get_currency_management_keyboard(i18n)
            )

    except Exception as e:
        logger.error(f"Error in handle_add_currency: {e}")
        await callback.message.edit_text(
            i18n.get("error-occurred"),
            reply_markup=back_to_menu_button(i18n)
        )

@currency_router.callback_query(F.data.startswith("remove_"))
async def handle_remove_currency(callback: CallbackQuery, i18n: TranslatorRunner):
    """Обрабатывает удаление валюты."""
    try:
        currency = callback.data.split("_")[1]
        user_id = callback.from_user.id
        
        async with get_db(user_id=user_id) as session:
            await remove_user_currency(session, user_id, currency)
            
            await callback.message.edit_text(
                i18n.get("currency-removed-successfully", currency=currency),
                reply_markup=get_currency_management_keyboard(i18n)
            )

    except Exception as e:
        logger.error(f"Error in handle_remove_currency: {e}")
        await callback.message.edit_text(
            i18n.get("error-occurred"),
            reply_markup=back_to_menu_button(i18n)
        )
