from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner
from database.database import get_db
from database.models import Alert, UserCurrency
from database.queries import get_user_alerts, get_user_currencies
from keyboards.inline import (
    get_alerts_keyboard,
    get_currency_selection_keyboard,
    back_to_menu_button
)
from states.alert_states import AlertStates
import logging
from sqlalchemy import select
from decimal import Decimal

logger = logging.getLogger(__name__)

alerts_router = Router()

@alerts_router.callback_query(F.data == "show_alerts")
async def show_alerts(callback: CallbackQuery, i18n: TranslatorRunner):
    """Показывает все алерты пользователя."""
    try:
        # Используем telegram_id для определения шарда
        async with get_db(user_id=callback.from_user.id) as session:
            alerts = await get_user_alerts(session, callback.from_user.id)
            
            if not alerts:
                await callback.message.edit_text(
                    i18n.get("no-alerts"),
                    reply_markup=get_alerts_keyboard(i18n)
                )
                return

            message_parts = [i18n.get("your-alerts"), ""]
            
            for alert in alerts:
                status = "✅" if alert.is_active else "❌"
                currency = alert.user_currency.currency
                threshold = float(alert.threshold)
                condition = ">" if alert.condition_type == "above" else "<"
                currency_type = alert.currency_type
                
                alert_text = f"{status} {currency} {condition} {threshold} {currency_type}"
                message_parts.append(alert_text)

            await callback.message.edit_text(
                "\n".join(message_parts),
                reply_markup=get_alerts_keyboard(i18n)
            )

    except Exception as e:
        logger.error(f"Error in show_alerts: {e}")
        await callback.message.edit_text(
            i18n.get("error-occurred"),
            reply_markup=back_to_menu_button(i18n)
        )

@alerts_router.callback_query(F.data == "add_alert")
async def start_add_alert(callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner):
    """Начинает процесс добавления нового алерта."""
    try:
        # Используем telegram_id для определения шарда
        async with get_db(user_id=callback.from_user.id) as session:
            currencies = await get_user_currencies(session, callback.from_user.id)
            
            if not currencies:
                await callback.message.edit_text(
                    i18n.get("no-currencies-for-alert"),
                    reply_markup=back_to_menu_button(i18n)
                )
                return

            await state.set_state(AlertStates.waiting_for_currency)
            await callback.message.edit_text(
                i18n.get("select-currency-for-alert"),
                reply_markup=get_currency_selection_keyboard(currencies, i18n)
            )

    except Exception as e:
        logger.error(f"Error in start_add_alert: {e}")
        await callback.message.edit_text(
            i18n.get("error-occurred"),
            reply_markup=back_to_menu_button(i18n)
        )

@alerts_router.callback_query(F.data.startswith("select_currency_"))
async def handle_currency_selection(callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner):
    """Обрабатывает выбор валюты для алерта."""
    currency_id = int(callback.data.split("_")[-1])
    
    try:
        # Используем telegram_id для определения шарда
        async with get_db(user_id=callback.from_user.id) as session:
            result = await session.execute(
                select(UserCurrency).where(UserCurrency.id == currency_id)
            )
            currency = result.scalar_one_or_none()
            
            if not currency:
                await callback.message.edit_text(
                    i18n.get("currency-not-found"),
                    reply_markup=back_to_menu_button(i18n)
                )
                return

            await state.update_data(currency_id=currency_id)
            await state.set_state(AlertStates.waiting_for_threshold)
            
            await callback.message.edit_text(
                i18n.get("enter-threshold-value"),
                reply_markup=back_to_menu_button(i18n)
            )

    except Exception as e:
        logger.error(f"Error in handle_currency_selection: {e}")
        await callback.message.edit_text(
            i18n.get("error-occurred"),
            reply_markup=back_to_menu_button(i18n)
        )

@alerts_router.message(AlertStates.waiting_for_threshold)
async def handle_threshold(message: Message, state: FSMContext, i18n: TranslatorRunner):
    """Обрабатывает ввод порогового значения для алерта."""
    try:
        threshold = Decimal(message.text.replace(",", "."))
        if threshold <= 0:
            await message.reply(i18n.get("invalid-threshold"))
            return

        state_data = await state.get_data()
        currency_id = state_data["currency_id"]

        # Используем telegram_id для определения шарда
        async with get_db(user_id=message.from_user.id) as session:
            # Создаем новый алерт
            alert = Alert(
                user_id=message.from_user.id,
                user_currency_id=currency_id,
                threshold=threshold,
                is_active=True
            )
            session.add(alert)
            await session.commit()

            await state.clear()
            await message.reply(
                i18n.get("alert-created"),
                reply_markup=get_alerts_keyboard(i18n)
            )

    except ValueError:
        await message.reply(i18n.get("invalid-number"))
    except Exception as e:
        logger.error(f"Error in handle_threshold: {e}")
        await message.reply(
            i18n.get("error-occurred"),
            reply_markup=back_to_menu_button(i18n)
        )
