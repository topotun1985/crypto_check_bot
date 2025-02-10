import logging
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner
from sqlalchemy import select, update

from database.database import get_db
from database.models import Alert, UserCurrency, User, CryptoRate, DollarRate
from database.queries import (
    get_user,
    get_user_currencies,
    get_alert_settings,
    add_alert,
    update_alert,
    delete_alert,
    get_user_currency_by_id,
    get_crypto_rate,
    get_dollar_rate
)
from keyboards.inline import get_new_alert_keyboard, get_threshold_input_keyboard, get_alert_settings_keyboard
from .start import back_to_menu  # Для правильной навигации

logger = logging.getLogger(__name__)
notification_router = Router()


class NotificationStates(StatesGroup):
    CHOOSING_CURRENCY = State()
    CHOOSING_CURRENCY_TYPE = State()  # USD or RUB
    ENTERING_THRESHOLD = State()


def get_notification_keyboard(currencies_with_alerts, i18n):
    builder = InlineKeyboardBuilder()
    
    # Split into columns if more than 10 currencies
    columns = 2 if len(currencies_with_alerts) > 10 else 1
    
    for currency, has_alerts in currencies_with_alerts:
        status = "✅" if has_alerts else "☑️"
        text = f"{status} {currency.currency}"
        builder.button(
            text=text,
            callback_data=f"alert_currency_{currency.id}"
        )
    
    builder.button(text=i18n.get("btn-back"), callback_data="back_to_main")
    builder.adjust(columns)
    return builder.as_markup()


def get_currency_settings_keyboard(currency_id: int, has_active_alerts: bool, i18n: TranslatorRunner):
    builder = InlineKeyboardBuilder()
    
    # Кнопка включения/выключения уведомлений
    if has_active_alerts:
        builder.button(
            text=i18n.get("button-disable-alerts"),
            callback_data=f"disable_alerts_{currency_id}"
        )
    else:
        builder.button(
            text=i18n.get("button-enable-alerts"),
            callback_data=f"enable_alerts_{currency_id}"
        )
    
    # Кнопки установки порогов
    builder.button(
        text=i18n.get("button-set-threshold-above"),
        callback_data=f"set_threshold_above_{currency_id}"
    )
    builder.button(
        text=i18n.get("button-set-threshold-below"),
        callback_data=f"set_threshold_below_{currency_id}"
    )
    
    # Кнопка назад
    builder.button(
        text=i18n.get("btn-back"),
        callback_data="back_to_currencies"
    )
    
    # Располагаем кнопки в столбик
    builder.adjust(1)
    return builder.as_markup()


@notification_router.callback_query(F.data == "notification_settings")
async def show_notification_menu(callback: CallbackQuery, i18n: TranslatorRunner):
    """Show the main notification settings menu with list of currencies"""
    try:
        async with get_db() as session:
            # Получаем пользователя, его валюты и алерты одним запросом
            result = await session.execute(
                select(UserCurrency, Alert)
                .outerjoin(Alert, UserCurrency.id == Alert.user_currency_id)
                .join(User, User.id == UserCurrency.user_id)
                .where(User.telegram_id == callback.from_user.id)
            )
            rows = result.all()
            
            if not rows:
                await callback.message.edit_text(
                    i18n.get("alerts-no-currencies"),
                    reply_markup=InlineKeyboardBuilder().button(
                        text=i18n.get("btn-back"),
                        callback_data="back_to_main"
                    ).as_markup()
                )
                return
            
            # Группируем результаты по валютам
            currencies_with_alerts = []
            current_currency = None
            has_active_alerts = False
            
            for currency, alert in rows:
                if current_currency != currency:
                    if current_currency is not None:
                        currencies_with_alerts.append((current_currency, has_active_alerts))
                    current_currency = currency
                    has_active_alerts = False
                
                if alert and alert.is_active:
                    has_active_alerts = True
            
            # Добавляем последнюю валюту
            if current_currency is not None:
                currencies_with_alerts.append((current_currency, has_active_alerts))
            
            keyboard = get_notification_keyboard(currencies_with_alerts, i18n)
            
            await callback.message.edit_text(
                i18n.get("alerts-choose-currency"),
                reply_markup=keyboard
            )
    except Exception as e:
        logger.error(f"Error in show_notification_menu: {str(e)}", exc_info=True)
        await callback.message.edit_text(
            i18n.get("error-occurred"),
            reply_markup=InlineKeyboardBuilder().button(
                text=i18n.get("btn-back"),
                callback_data="back_to_main"
            ).as_markup()
        )


@notification_router.callback_query(F.data.startswith("alert_currency_"))
async def show_currency_settings(callback: CallbackQuery, i18n: TranslatorRunner, currency_id: int = None):
    """Show settings for a specific currency"""
    try:
        if currency_id is None:
            currency_id = int(callback.data.split("_")[2])
        
        async with get_db() as session:
            # Получаем пользователя и его валюту
            result = await session.execute(
                select(User, UserCurrency)
                .join(UserCurrency, User.id == UserCurrency.user_id)
                .where(User.telegram_id == callback.from_user.id)
                .where(UserCurrency.id == currency_id)
            )
            row = result.first()
            if not row:
                await callback.answer(i18n.get("currency-not-found"))
                return
                
            user, currency = row
            
            # Получаем курс криптовалюты
            crypto_result = await session.execute(
                select(CryptoRate)
                .where(CryptoRate.currency == currency.currency)
            )
            crypto_rate = crypto_result.scalar_one_or_none()
            
            # Получаем курс доллара
            dollar_result = await session.execute(
                select(DollarRate)
                .order_by(DollarRate.id.desc())
                .limit(1)
            )
            dollar_rate = dollar_result.scalar_one_or_none()
            
            # Получаем все алерты для валюты
            alerts_result = await session.execute(
                select(Alert)
                .where(Alert.user_currency_id == currency_id)
                .order_by(Alert.condition_type.desc())  # above будет первым
            )
            all_alerts = alerts_result.scalars().all()
            
            # Формируем сообщение о цене
            price_msg = []
            if crypto_rate:
                price_msg.append(i18n.get("alerts-list-header", currency=currency.currency))
                price_msg.append("")
                if user.language == "ru" and dollar_rate:
                    price_rub = crypto_rate.price * dollar_rate.price
                    price_msg.append(i18n.get("alerts-current-price")+f"\n{crypto_rate.price:.2f} $⁨\n{price_rub:.2f} ₽⁩")
                    price_msg.append("")
                else:
                    price_msg.append(i18n.get("alerts-current-price")+f" {crypto_rate.price:.2f} $⁨")
                    price_msg.append("")
            
            # Формируем сообщение об алертах
            alert_msg = []
            alert_msg.append(i18n.get("alerts-current-settings"))
            alert_msg.append("")
            
            # Проверяем есть ли активные алерты
            has_active_alerts = any(alert.is_active for alert in all_alerts)
            alert_msg.append(i18n.get("alerts-notifications-enabled") if has_active_alerts else i18n.get("alerts-notifications-disabled"))
            alert_msg.append("")
            
            # Группируем алерты по валюте (учитываем регистр)
            usd_alerts = {alert.condition_type: alert for alert in all_alerts if alert.currency_type.upper() == "USD"}
            rub_alerts = {alert.condition_type: alert for alert in all_alerts if alert.currency_type.upper() == "RUB"}
            
            # Показываем USD алерты
            alert_msg.append(i18n.get("alerts-usd-header"))
            alert_msg.append("")
            alert_msg.append(i18n.get("alerts-threshold-above") + " " + (f"⁨{usd_alerts['above'].threshold:.2f}⁩" if "above" in usd_alerts and usd_alerts['above'].is_active else i18n.get("alerts-not-set")))
            alert_msg.append(i18n.get("alerts-threshold-below") + " " + (f"⁨{usd_alerts['below'].threshold:.2f}⁩" if "below" in usd_alerts and usd_alerts['below'].is_active else i18n.get("alerts-not-set")))
            alert_msg.append("")
            
            # Показываем RUB алерты только для русскоязычных пользователей
            if user.language == "ru":
                alert_msg.append(i18n.get("alerts-rub-header"))
                alert_msg.append("")
                alert_msg.append(i18n.get("alerts-threshold-above") + " " + (f"⁨{rub_alerts['above'].threshold:.2f}⁩" if "above" in rub_alerts and rub_alerts['above'].is_active else i18n.get("alerts-not-set")))
                alert_msg.append(i18n.get("alerts-threshold-below") + " " + (f"⁨{rub_alerts['below'].threshold:.2f}⁩" if "below" in rub_alerts and rub_alerts['below'].is_active else i18n.get("alerts-not-set")))
                alert_msg.append("")
        
            # Формируем итоговое сообщение
            message = "\n".join([
                "\n".join(price_msg),
                "\n".join(alert_msg)
            ])
            
            # Создаем клавиатуру и отправляем сообщение
            has_active_alerts = any(alert.is_active for alert in all_alerts)
            keyboard = get_currency_settings_keyboard(currency_id=currency.id, has_active_alerts=has_active_alerts, i18n=i18n)
            try:
                await callback.message.edit_text(message, reply_markup=keyboard)
            except TelegramBadRequest as e:
                if "message is not modified" not in str(e):
                    raise
            
    except ValueError as e:
        logger.error(f"Invalid currency_id in show_currency_settings: {str(e)}")
        await callback.answer(i18n.get("error-occurred"))
        await callback.answer(i18n.get("error-invalid-currency"))
    except Exception as e:
        logger.error(f"Error in show_currency_settings: {str(e)}", exc_info=True)
        await callback.message.edit_text(
            i18n.get("error-occurred"),
            reply_markup=InlineKeyboardBuilder().button(
                text=i18n.get("btn-back"),
                callback_data="back_to_currencies"
            ).as_markup()
        )


def get_currency_type_keyboard(i18n: TranslatorRunner, currency_id: int, condition_type: str) -> InlineKeyboardMarkup:
    """Create keyboard for selecting currency type (USD/RUB) for threshold."""
    builder = InlineKeyboardBuilder()
    
    # Add USD button
    builder.button(
        text=i18n.get("button-set-threshold-usd"),
        callback_data=f"set_currency_type_{currency_id}_{condition_type}_USD"
    )
    
    # Add RUB button
    builder.button(
        text=i18n.get("button-set-threshold-rub"),
        callback_data=f"set_currency_type_{currency_id}_{condition_type}_RUB"
    )
    
    # Add back button
    builder.button(
        text=i18n.get("btn-back"),
        callback_data=f"back_to_settings_{currency_id}"
    )
    
    # Arrange buttons in a column
    builder.adjust(1)
    return builder.as_markup()


def get_threshold_input_keyboard(i18n: TranslatorRunner, currency_id: int, condition_type: str, currency_type: str) -> InlineKeyboardMarkup:
    """Create keyboard for threshold input with back button."""
    builder = InlineKeyboardBuilder()
    
    # Add back button that returns to currency type selection
    builder.button(
        text=i18n.get("btn-back"),
        callback_data=f"set_threshold_{condition_type}_{currency_id}"
    )
    
    # Arrange buttons in a column
    builder.adjust(1)
    return builder.as_markup()


@notification_router.callback_query(F.data.startswith(("set_threshold_above_", "set_threshold_below_")))
async def handle_set_threshold(callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner):
    try:
        # Parse callback data
        parts = callback.data.split("_")
        condition_type = parts[2]  # 'above' or 'below'
        currency_id = int(parts[3])
        
        # Save data to state
        await state.update_data(currency_id=currency_id, condition_type=condition_type)
        
        # Set state
        await state.set_state(NotificationStates.CHOOSING_CURRENCY_TYPE)
        
        # Get keyboard
        keyboard = get_currency_type_keyboard(i18n, currency_id, condition_type)
        
        # Get current price
        async with get_db() as session:
            # Get user currency
            result = await session.execute(
                select(User, UserCurrency)
                .join(UserCurrency, User.id == UserCurrency.user_id)
                .where(User.telegram_id == callback.from_user.id)
                .where(UserCurrency.id == currency_id)
            )
            row = result.first()
            if not row:
                await callback.answer(i18n.get("currency-not-found"))
                return
            
            user, user_currency = row
            
            # Get crypto rate
            crypto_rate = await get_crypto_rate(session, user_currency.currency)
            if not crypto_rate:
                await callback.answer(i18n.get("rate-not-found"))
                return
            
            # Get dollar rate
            dollar_rate = await get_dollar_rate(session)
            
            # Calculate prices
            current_price_usd = crypto_rate.price
            current_price_rub = current_price_usd * dollar_rate.price if dollar_rate else 0
        
        # Show message with current price and currency type selection
        message = i18n.get("select-currency-type")
        await callback.message.edit_text(
            message + "\n\n" +
            i18n.get("alerts-current-price")+f"\n{current_price_usd:.2f} $⁨\n{current_price_rub:.2f} ₽⁩",
            reply_markup=keyboard
        )
        
    except Exception as e:
        logger.error(f"Error in handle_set_threshold: {str(e)}", exc_info=True)
        await callback.message.edit_text(
            i18n.get("error-occurred"),
            reply_markup=InlineKeyboardBuilder().button(
                text=i18n.get("btn-back"),
                callback_data="back_to_currencies"
            ).as_markup()
        )


@notification_router.callback_query(F.data.startswith("set_currency_type_"))
async def handle_currency_type_selection(callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner):
    """Handle currency type selection (USD/RUB)"""
    try:
        # Parse callback data
        parts = callback.data.split("_")
        # Format: set_currency_type_<currency_id>_<condition_type>_<currency_type>
        currency_id = int(parts[3])
        condition_type = parts[4]
        currency_type = parts[5].lower()
        
        # Save data to state
        await state.update_data({
            "currency_id": currency_id,
            "condition_type": condition_type,
            "currency_type": currency_type
        })
        
        # Set state
        await state.set_state(NotificationStates.ENTERING_THRESHOLD)
        
        # Get keyboard
        keyboard = get_threshold_input_keyboard(i18n, currency_id, condition_type, currency_type)
        
        # Get current price
        async with get_db() as session:
            # Get user currency
            result = await session.execute(
                select(User, UserCurrency)
                .join(UserCurrency, User.id == UserCurrency.user_id)
                .where(User.telegram_id == callback.from_user.id)
                .where(UserCurrency.id == currency_id)
            )
            row = result.first()
            if not row:
                await callback.answer(i18n.get("currency-not-found"))
                return
            
            user, user_currency = row
            
            # Get crypto rate
            crypto_rate = await get_crypto_rate(session, user_currency.currency)
            if not crypto_rate:
                await callback.answer(i18n.get("rate-not-found"))
                return
            
            # Get dollar rate
            dollar_rate = await get_dollar_rate(session)
            
            # Calculate prices
            current_price_usd = crypto_rate.price
            current_price_rub = current_price_usd * dollar_rate.price if dollar_rate else 0
            
            # Format price based on selected currency type
            if currency_type.lower() == "usd":
                price_display = f"{current_price_usd:.2f} $"
            else:
                price_display = f"{current_price_rub:.2f} ₽"
            
            # Show message with current price and threshold input prompt
            try:
                await callback.message.edit_text(
                    i18n.get("enter-threshold-value") + "\n\n" +
                    i18n.get("alerts-current-price")+f" ⁨ {price_display} ⁩",
                    reply_markup=keyboard
                )
            except TelegramBadRequest as e:
                if "message is not modified" not in str(e):
                    raise
                await callback.answer()
            
    except Exception as e:
        logger.error(f"Error in handle_currency_type_selection: {str(e)}", exc_info=True)
        await callback.message.edit_text(
            i18n.get("error-occurred"),
            reply_markup=InlineKeyboardBuilder().button(
                text=i18n.get("btn-back"),
                callback_data=f"set_threshold_{currency_id}_{condition_type}"
            ).as_markup()
        )
        await state.clear()


@notification_router.message(NotificationStates.ENTERING_THRESHOLD)
async def handle_threshold_input(message: Message, state: FSMContext, i18n: TranslatorRunner):
    """Handle threshold value input"""
    try:
        # Get state data
        data = await state.get_data()
        currency_id = data.get("currency_id")
        condition_type = data.get("condition_type")
        currency_type = data.get("currency_type")
        
        # Check if we have all required data
        if not all([currency_id, condition_type, currency_type]):
            logger.error(f"Missing state data: {data}")
            await message.answer(
                i18n.get("error-occurred"),
                reply_markup=InlineKeyboardBuilder().button(
                    text=i18n.get("btn-back"),
                    callback_data="back_to_main"
                ).as_markup()
            )
            await state.clear()
            return
        
        # Parse threshold value
        try:
            threshold = float(message.text)
            if threshold <= 0:
                raise ValueError("Threshold must be positive")
        except ValueError:
            await message.answer(
                i18n.get("invalid-threshold-value"),
                reply_markup=get_threshold_input_keyboard(i18n, currency_id, condition_type, currency_type).as_markup()
            )
            return
        
        # Get current price and validate threshold
        async with get_db() as session:
            user_currency = await get_user_currency_by_id(session, currency_id)
            if not user_currency:
                await message.answer(i18n.get("currency-not-found"))
                return
            
            crypto_rate = await get_crypto_rate(session, user_currency.currency)
            if not crypto_rate:
                await message.answer(i18n.get("rate-not-found"))
                return
            
            dollar_rate = await get_dollar_rate(session)
            
            current_price_usd = crypto_rate.price
            current_price_rub = current_price_usd * dollar_rate.price if dollar_rate else 0
            
            # Get appropriate price based on selected currency type
            current_price = current_price_usd if currency_type == "usd" else current_price_rub
            
            # Get user
            user = await get_user(session, message.from_user.id)
            if not user:
                await message.answer(i18n.get("user-not-found"))
                return

            # Check if alert already exists for this combination
            existing_alerts = await session.execute(
                select(Alert)
                .where(
                    Alert.user_id == user.id,
                    Alert.user_currency_id == currency_id,
                    Alert.condition_type == condition_type,
                    Alert.currency_type == currency_type.lower()  # Ensure case consistency
                )
            )
            existing_alerts = existing_alerts.scalars().all()
            
            # If multiple alerts exist, we'll update the first one and delete the rest
            if len(existing_alerts) > 1:
                logger.warning(f"Found {len(existing_alerts)} alerts for the same condition, cleaning up...")
                existing_alert = existing_alerts[0]
                # Delete duplicate alerts
                for alert in existing_alerts[1:]:
                    await session.delete(alert)
            elif len(existing_alerts) == 1:
                existing_alert = existing_alerts[0]
            else:
                existing_alert = None
            
            if existing_alert:
                # Update existing alert
                existing_alert.threshold = threshold
                existing_alert.is_active = True
                existing_alert.updated_at = datetime.utcnow()
                alert = existing_alert  # For message formatting below
            else:
                # Create new alert only if one doesn't exist
                alert = Alert(
                    user_id=user.id,
                    user_currency_id=currency_id,
                    condition_type=condition_type,
                    threshold=threshold,
                    currency_type=currency_type.lower(),  # Ensure case consistency
                    is_active=True
                )
                session.add(alert)
            
            await session.commit()
            
            # Format message with current price and threshold
            symbol = "$" if currency_type == "usd" else "₽"
            condition_text = "above" if condition_type == "above" else "below"
            
            # Show success message
            success_msg = i18n.get("alert-updated-successfully") if existing_alert else i18n.get("alert-added-successfully")
            if not success_msg:  # Fallback if translation is missing
                success_msg = i18n.get("alert-updated-successfully") if existing_alert else i18n.get("alert-added-successfully")
            
            details_msg = i18n.get("alert-details", 
                currency=user_currency.currency,
                condition=condition_text,
                threshold=f"{symbol}{threshold:.2f}",
                current_price=f"{symbol}{current_price:.2f}"
            )
            if not details_msg:  # Fallback if translation is missing
                details_msg = f"Currency: {user_currency.currency}\nCondition: {condition_text}\nThreshold: {symbol}{threshold:.2f}\nCurrent price: {symbol}{current_price:.2f}"
            
            await message.answer(
                f"{success_msg}\n\n{details_msg}",
                reply_markup=InlineKeyboardBuilder().button(
                    text=i18n.get("btn-back"),
                    callback_data=f"back_to_settings_{currency_id}"
                ).as_markup()
            )
        
        # Clear state
        await state.clear()
        
    except ValueError as e:
        logger.error(f"Invalid threshold value: {str(e)}")
        try:
            keyboard = get_threshold_input_keyboard(
                i18n, 
                int(data.get("currency_id", 0)), 
                data.get("condition_type", ""), 
                data.get("currency_type", "")
            ).as_markup()
        except Exception as ke:
            logger.error(f"Error creating keyboard: {str(ke)}")
            keyboard = InlineKeyboardBuilder().button(
                text=i18n.get("btn-back") or "Back",
                callback_data="back_to_main"
            ).as_markup()
        
        await message.answer(
            i18n.get("invalid-threshold-value"),
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Error in handle_threshold_input: {str(e)}", exc_info=True)
        await message.answer(
            i18n.get("error-occurred"),
            reply_markup=InlineKeyboardBuilder().button(
                text=i18n.get("btn-back") or "Back",
                callback_data="back_to_main"
            ).as_markup()
        )
        await state.clear()


@notification_router.callback_query(F.data == "delete_alerts")
async def delete_currency_alerts(callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner):
    """Delete all alerts for the current currency"""
    data = await state.get_data()
    currency_id = int(data.get("currency_id", 0))
    
    async with get_db() as session:
        await delete_alert(session, user_id=callback.from_user.id, user_currency_id=currency_id)
        await show_currency_settings(callback, i18n)

# Add navigation handlers
@notification_router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner):
    await state.clear()
    await back_to_menu(callback, i18n)

    
@notification_router.callback_query(F.data == "back_to_currencies")
async def back_to_currencies(callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner):
    await state.clear()
    await show_notification_menu(callback, i18n)


@notification_router.callback_query(F.data.startswith("back_to_settings_"))
async def back_to_settings(callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner):
    try:
        # Get currency ID from callback data
        currency_id = int(callback.data.split("_")[3])
        
        # Clear state
        await state.clear()
        
        # Show currency settings
        await show_currency_settings(callback, i18n, currency_id=currency_id)
    except Exception as e:
        logger.error(f"Error in back_to_settings: {str(e)}", exc_info=True)
        await callback.message.edit_text(
            i18n.get("error-occurred"),
            reply_markup=InlineKeyboardBuilder().button(
                text=i18n.get("btn-back"),
                callback_data="back_to_main"
            ).as_markup()
        )


@notification_router.callback_query(F.data.startswith("back_to_condition_"))
async def back_to_condition(callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner):
    try:
        # Get currency ID from callback data
        currency_id = int(callback.data.split("_")[3])
        
        # Set state back to condition selection
        await state.set_state(NotificationStates.CHOOSING_CONDITION)
        await state.update_data({"currency_id": currency_id})
        
        # Show condition selection keyboard with back button
        keyboard = get_condition_keyboard(i18n, currency_id)
        message = i18n.get("select-condition")
        await callback.message.edit_text(
            message,
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Error in back_to_condition: {str(e)}", exc_info=True)
        await callback.message.edit_text(
            i18n.get("error-occurred"),
            reply_markup=InlineKeyboardBuilder().button(
                text=i18n.get("btn-back"),
                callback_data="back_to_main"
            ).as_markup()
        )


@notification_router.callback_query(F.data.startswith("set_new_threshold_"))
async def handle_set_new_threshold(callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner):
    """Обработка нажатия кнопки установки нового порога"""
    try:
        alert_id = int(callback.data.split("_")[3])
        
        async with get_db() as session:
            # Получаем алерт и связанные данные
            result = await session.execute(
                select(Alert, UserCurrency)
                .join(UserCurrency, Alert.user_currency_id == UserCurrency.id)
                .where(Alert.id == alert_id)
            )
            row = result.first()
            if not row:
                await callback.answer(i18n.get("alert-not-found"))
                return
                
            alert, user_currency = row
            
            # Сохраняем данные в состоянии
            await state.update_data(
                alert_id=alert_id,
                currency_id=user_currency.id,
                condition_type=alert.condition_type,
                currency_type=alert.currency_type
            )
            
            # Переходим к вводу нового порога
            await state.set_state(NotificationStates.ENTERING_THRESHOLD)
            
            # Создаем клавиатуру для ввода порога
            keyboard = get_threshold_input_keyboard(i18n, user_currency.id, alert.condition_type, alert.currency_type)
            
            await callback.message.edit_text(
                i18n.get("enter-new-threshold", 
                        currency=user_currency.currency,
                        currency_type=alert.currency_type),
                reply_markup=keyboard
            )
            
    except ValueError as e:
        logger.error(f"Invalid alert_id in handle_set_new_threshold: {str(e)}")
        await callback.answer(i18n.get("error-invalid-alert"))
    except Exception as e:
        logger.error(f"Error in handle_set_new_threshold: {str(e)}", exc_info=True)
        await callback.answer(i18n.get("error-occurred"))


@notification_router.callback_query(F.data.startswith("disable_alerts_"))
async def handle_disable_alert(callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner):
    """Обработка нажатия кнопки отключения уведомления"""
    try:
        # Extract currency_id from callback data
        try:
            currency_id = int(callback.data.split("_")[2])
        except (ValueError, IndexError):
            logger.error(f"Invalid callback data format: {callback.data}")
            await callback.answer(i18n.get("error-occurred"))
            return
        
        async with get_db() as session:
            # Get user and currency
            result = await session.execute(
                select(User, UserCurrency)
                .join(UserCurrency, User.id == UserCurrency.user_id)
                .where(User.telegram_id == callback.from_user.id)
                .where(UserCurrency.id == currency_id)
            )
            row = result.first()
            if not row:
                logger.error(f"Currency not found: {currency_id} for user {callback.from_user.id}")
                await callback.answer(i18n.get("currency-not-found"))
                return
            
            user, user_currency = row
            
            # Get alerts for this currency
            result = await session.execute(
                select(Alert)
                .where(Alert.user_currency_id == user_currency.id)
            )
            alerts = result.scalars().all()
            
            if not alerts:
                logger.warning(f"No alerts found for currency {currency_id}")
                await callback.answer(i18n.get("no-alerts-to-disable"))
                return
            
            # Disable all alerts for this currency
            await session.execute(
                update(Alert)
                .where(Alert.user_currency_id == user_currency.id)
                .values(is_active=False)
            )
            await session.commit()
            
            # Show success message
            await callback.answer(
                i18n.get("alerts-disabled-successfully") or "Alerts disabled successfully"
            )
            
            # Update the settings view
            await show_currency_settings(callback, i18n, user_currency.id)
            
    except Exception as e:
        logger.error(f"Error in handle_disable_alert: {str(e)}", exc_info=True)
        await callback.answer(i18n.get("error-occurred"))
        await state.clear()


@notification_router.callback_query(F.data.startswith("enable_alerts_"))
async def handle_enable_alerts(callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner):
    """Обработка нажатия кнопки включения уведомлений"""
    try:
        # Get currency_id from callback data (enable_alerts_<currency_id>)
        currency_id = int(callback.data.split("_")[2])
        
        async with get_db() as session:
            # Get user currency first
            result = await session.execute(
                select(UserCurrency)
                .where(
                    UserCurrency.id == currency_id,
                    UserCurrency.user_id == callback.from_user.id
                )
            )
            user_currency = result.scalar_one_or_none()
            if not user_currency:
                # Show message that user needs to set thresholds first
                await callback.answer(i18n.get("alerts-no-thresholds"), show_alert=True)
                return

            # Check if there are existing alerts
            result = await session.execute(
                select(Alert)
                .where(
                    Alert.user_currency_id == currency_id
                )
            )
            alerts = result.scalars().all()
            
            if not alerts:
                # Show message that user needs to set thresholds first
                await callback.answer(i18n.get("alerts-no-thresholds"), show_alert=True)
                return
            
            # Enable existing alerts
            for alert in alerts:
                alert.is_active = True
                alert.updated_at = datetime.utcnow()
            
            await session.commit()
            
            # Clear state and show updated settings
            await state.clear()
            await show_currency_settings(callback, i18n, currency_id)
            
    except ValueError as e:
        logger.error(f"Invalid currency_id in handle_enable_alerts: {str(e)}")
        await callback.answer(i18n.get("error-invalid-alert"))
    except Exception as e:
        logger.error(f"Error in handle_enable_alerts: {str(e)}", exc_info=True)
        await callback.answer(i18n.get("error-occurred"))


async def check_alert_conditions(bot, i18n):
    """Проверяет условия для алертов и отправляет уведомления."""
    async with get_db() as session:
        try:
            # Получаем курс доллара
            usd_rate_result = await session.execute(select(DollarRate))
            usd_rate = usd_rate_result.scalar_one_or_none()
            if not usd_rate:
                logger.error("USD rate not found")
                return

            # Получаем все активные алерты с информацией о пользователях и валютах
            result = await session.execute(
                select(Alert, UserCurrency, User)
                .join(UserCurrency, Alert.user_currency_id == UserCurrency.id)
                .join(User, UserCurrency.user_id == User.id)
                .where(Alert.is_active == True)
                .where(Alert.last_triggered_at.is_(None) | 
                       (datetime.utcnow() - Alert.last_triggered_at > timedelta(minutes=5)))
            )
            alerts = result.all()
            
            # Получаем все курсы криптовалют
            crypto_rates_result = await session.execute(select(CryptoRate))
            crypto_rates = {rate.currency: rate.price for rate in crypto_rates_result.scalars().all()}

            for alert, user_currency, user in alerts:
                try:
                    crypto_price = crypto_rates.get(user_currency.currency)
                    if not crypto_price:
                        logger.error(f"No price found for {user_currency.currency}")
                        continue

                    # Конвертируем в нужную валюту
                    price_in_currency = crypto_price
                    threshold_in_currency = alert.threshold
                    if alert.currency_type.upper() == 'RUB':
                        price_in_currency *= usd_rate.price
                        # Порог уже в рублях
                    else:
                        # Если валюта USD, оставляем цену как есть
                        price_in_currency = crypto_price
                    
                    # Проверяем условие
                    condition_met = False
                    logger.info(f"Checking alert {alert.id} for {user_currency.currency}:")
                    logger.info(f"Current price: {price_in_currency} {alert.currency_type.upper()}")
                    logger.info(f"Threshold: {threshold_in_currency} {alert.currency_type.upper()}")
                    logger.info(f"Condition: {alert.condition_type}")
                    logger.info(f"Last triggered: {alert.last_triggered_at}")
                    
                    if alert.condition_type == 'above' and price_in_currency > threshold_in_currency:
                        condition_met = True
                        logger.info("Above condition met")
                    elif alert.condition_type == 'below' and price_in_currency < threshold_in_currency:
                        condition_met = True
                        logger.info("Below condition met")

                    if condition_met:
                        # Формируем сообщение
                        currency_symbol = 'RUB' if alert.currency_type.upper() == 'RUB' else 'USD'
                        direction = i18n.get("alert-price-above") if alert.condition_type == 'above' else i18n.get("alert-price-below")
                        message = (
                            f"🔔 {user_currency.currency}\n"+
                            i18n.get("alert-price")+f" {direction} {alert.threshold:.2f} {currency_symbol}\n"+
                            i18n.get("alerts-current-price")+f" {price_in_currency:.2f} {currency_symbol}"
                        )
                        
                        # Создаем клавиатуру для установки нового порога
                        keyboard = get_new_alert_keyboard(i18n, alert.id, user_currency.currency)
                        
                        try:
                            # Отправляем уведомление
                            sent_message = await bot.send_message(
                                user.telegram_id,
                                message,
                                reply_markup=keyboard
                            )
                            
                            if sent_message:
                                # Обновляем время последнего срабатывания
                                alert.last_triggered_at = datetime.utcnow()
                                alert.is_active = False  # Деактивируем алерт
                                await session.commit()
                                
                        except Exception as e:
                            logger.error(f"Failed to send notification: {str(e)}")
                            continue
                        logger.info(f"Alert notification sent to user {user.telegram_id} for {user_currency.currency}")

                except Exception as e:
                    logger.error(f"Error processing alert {alert.id}: {str(e)}", exc_info=True)

        except Exception as e:
            logger.error(f"Error in check_alert_conditions: {str(e)}", exc_info=True)
