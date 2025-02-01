from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from fluentogram import TranslatorRunner
from aiogram.exceptions import TelegramBadRequest
import logging
import re

from database.database import get_db
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
from keyboards.inline import (
    get_alerts_list_keyboard,
    get_alert_settings_keyboard,
    get_currency_choice_keyboard,
    get_percent_type_keyboard,
    back_to_menu_button
)

logger = logging.getLogger(__name__)
alerts_router = Router()

# Регулярные выражения для проверки callback_data
CURRENCY_ID_PATTERN = re.compile(r'^alert_currency_\d+$')
CURRENCY_CHOICE_PATTERN = re.compile(r'^alert_currency_choice_(usd|rub)_\d+$')
PERCENT_TYPE_PATTERN = re.compile(r'^alert_percent_type_(up|down|both)_\d+$')

class AlertStates(StatesGroup):
    """Состояния для настройки уведомлений."""
    waiting_for_threshold = State()  # Ожидание ввода порогового значения
    waiting_for_percent = State()    # Ожидание ввода процента изменения
    choosing_currency = State()      # Выбор валюты для порога

async def edit_or_send_message(message, text: str, reply_markup=None):
    """Пытается отредактировать сообщение, если не получается - отправляет новое."""
    try:
        await message.edit_text(text, reply_markup=reply_markup)
    except TelegramBadRequest as e:
        if "message can't be edited" in str(e):
            await message.answer(text, reply_markup=reply_markup)
        else:
            raise

@alerts_router.callback_query(lambda c: CURRENCY_ID_PATTERN.match(c.data))
async def show_currency_alerts(callback: CallbackQuery, i18n: TranslatorRunner):
    """Показывает настройки уведомлений для выбранной валюты."""
    try:
        logger.info("Entering show_currency_alerts handler")
        currency_id = int(callback.data.split("_")[2])
        
        async with get_db() as session:
            # Получаем пользователя и его язык
            user = await get_user(session, callback.from_user.id)
            
            # Получаем валюту
            currency = await get_user_currency_by_id(session, currency_id)
            if not currency:
                logger.error(f"Currency not found: {currency_id}")
                await edit_or_send_message(
                    callback.message,
                    i18n.get("alerts-currency-not-found"),
                    reply_markup=back_to_menu_button(i18n)
                )
                return
            
            # Получаем настройки уведомлений
            alert = await get_alert_settings(session, currency_id)
            
            # Получаем текущие курсы
            crypto_rate = await get_crypto_rate(session, currency.currency)
            dollar_rate = await get_dollar_rate(session)
            
            # Формируем сообщение
            message = [
                i18n.get("alerts-settings-header", currency=currency.currency),
                ""
            ]
            
            # Добавляем текущий курс
            if crypto_rate:
                if user.language == "ru" and dollar_rate:
                    price_rub = crypto_rate.price * dollar_rate.price
                    message.append(i18n.get("alerts-current-price-both",
                                          price_usd=f"{crypto_rate.price:.2f}",
                                          price_rub=f"{price_rub:.2f}"))
                else:
                    message.append(i18n.get("alerts-current-price",
                                          price=f"{crypto_rate.price:.2f}"))
                message.append("")
            
            # Добавляем текущие настройки
            message.append(i18n.get("alerts-current-settings"))
            message.append("")
            
            if alert and alert.is_active:
                message.append(i18n.get("alerts-notifications-enabled"))
            else:
                message.append(i18n.get("alerts-notifications-disabled"))
            message.append("")
            
            if alert and alert.threshold:
                if user.language == "ru":
                    if alert.in_rub and dollar_rate:
                        message.append(i18n.get("alerts-threshold-rub",
                                              threshold_rub=f"{alert.threshold:.2f}"))
                    else:
                        message.append(i18n.get("alerts-threshold-usd",
                                              threshold_usd=f"{alert.threshold:.2f}"))
                else:
                    message.append(i18n.get("alerts-threshold-usd",
                                          threshold_usd=f"{alert.threshold:.2f}"))
            else:
                message.append(i18n.get("alerts-threshold-not-set"))
            message.append("")
            
            if alert and alert.percent_change:
                message.append(i18n.get("alerts-percent-change",
                                      percent=alert.percent_change))
            else:
                message.append(i18n.get("alerts-percent-not-set"))
            
            logger.info("Sending message with currency alerts settings")
            await edit_or_send_message(
                callback.message,
                "\n".join(message),
                reply_markup=get_alert_settings_keyboard(i18n, currency_id, alert, user.language)
            )
            
    except Exception as e:
        logger.error(f"Error in show_currency_alerts: {str(e)}", exc_info=True)
        await edit_or_send_message(
            callback.message,
            i18n.get("alerts-error"),
            reply_markup=back_to_menu_button(i18n)
        )

@alerts_router.callback_query(lambda c: CURRENCY_CHOICE_PATTERN.match(c.data))
async def process_currency_choice(callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner):
    """Обрабатывает выбор валюты для порога."""
    try:
        logger.info("Entering process_currency_choice handler")
        parts = callback.data.split("_")
        choice = parts[3]  # usd или rub
        currency_id = int(parts[4])  # ID валюты
        
        in_rub = choice == "rub"
        
        await state.update_data(in_rub=in_rub, currency_id=currency_id)
        await state.set_state(AlertStates.waiting_for_threshold)
        
        message_key = "alerts-enter-threshold-rub" if in_rub else "alerts-enter-threshold-usd"
        await edit_or_send_message(
            callback.message,
            i18n.get(message_key),
            reply_markup=back_to_menu_button(i18n)
        )
    except Exception as e:
        logger.error(f"Error in process_currency_choice: {str(e)}", exc_info=True)
        await edit_or_send_message(
            callback.message,
            i18n.get("alerts-error"),
            reply_markup=back_to_menu_button(i18n)
        )

@alerts_router.callback_query(F.data == "show_alerts")
async def show_alerts_list(callback: CallbackQuery, i18n: TranslatorRunner):
    """Показывает список валют для настройки уведомлений."""
    try:
        logger.info("Entering show_alerts_list handler")
        async with get_db() as session:
            # Получаем пользователя
            user = await get_user(session, callback.from_user.id)
            if not user:
                logger.error(f"User not found: {callback.from_user.id}")
                await edit_or_send_message(
                    callback.message,
                    i18n.get("alerts-error"),
                    reply_markup=back_to_menu_button(i18n)
                )
                return
            
            # Получаем список валют пользователя
            currencies = await get_user_currencies(session, callback.from_user.id)
            logger.info(f"Found {len(currencies) if currencies else 0} currencies for user")
            
            if not currencies:
                await edit_or_send_message(
                    callback.message,
                    i18n.get("alerts-no-currencies"),
                    reply_markup=back_to_menu_button(i18n)
                )
                return
            
            # Для каждой валюты получаем настройки уведомлений
            currency_alerts = []
            for currency in currencies:
                alert = await get_alert_settings(session, currency.id)
                currency_alerts.append((currency, alert))
                logger.info(f"Currency {currency.currency}: alert {'exists' if alert else 'not found'}")
            
            # Формируем сообщение
            message = [i18n.get("alerts-list-header"), ""]
            message.append(i18n.get("alerts-choose-currency"))
            
            logger.info("Sending message with alerts list")
            await edit_or_send_message(
                callback.message,
                "\n".join(message),
                reply_markup=get_alerts_list_keyboard(i18n, currency_alerts)
            )
            
    except Exception as e:
        logger.error(f"Error in show_alerts_list: {str(e)}", exc_info=True)
        await edit_or_send_message(
            callback.message,
            i18n.get("alerts-error"),
            reply_markup=back_to_menu_button(i18n)
        )

@alerts_router.callback_query(F.data.startswith("alert_toggle_"))
async def toggle_alert(callback: CallbackQuery, i18n: TranslatorRunner):
    """Включает/выключает уведомления."""
    try:
        logger.info("Entering toggle_alert handler")
        currency_id = int(callback.data.split("_")[2])
        async with get_db() as session:
            currency = await get_user_currency_by_id(session, currency_id)
            alert = await get_alert_settings(session, currency_id)
            
            if alert:
                # Если алерт существует, переключаем его статус
                is_active = not alert.is_active
                await update_alert(session, alert.id, is_active=is_active)
            else:
                # Если алерта нет, создаем новый
                alert = await add_alert(session, currency_id, None, None)
                is_active = True
                await update_alert(session, alert.id, is_active=is_active)
            
            await session.commit()
            
            # Показываем сообщение об успехе
            message = i18n.get("alerts-enabled" if is_active else "alerts-disabled",
                             currency=currency.currency)
            await callback.answer(message)
            
            # Обновляем сообщение с настройками
            await show_currency_alerts(callback, i18n)
            
    except Exception as e:
        logger.error(f"Error in toggle_alert: {str(e)}", exc_info=True)
        await edit_or_send_message(
            callback.message,
            i18n.get("alerts-error"),
            reply_markup=back_to_menu_button(i18n)
        )

@alerts_router.callback_query(F.data.startswith("alert_set_threshold_"))
async def start_set_threshold(callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner):
    """Начинает процесс установки порогового значения."""
    try:
        logger.info("Entering start_set_threshold handler")
        currency_id = int(callback.data.split("_")[3])
        
        async with get_db() as session:
            user = await get_user(session, callback.from_user.id)
            
            # Для русского языка показываем выбор валюты
            if user.language == "ru":
                await state.set_state(AlertStates.choosing_currency)
                await state.update_data(currency_id=currency_id)
                
                await edit_or_send_message(
                    callback.message,
                    i18n.get("alerts-choose-currency-usd-rub"),
                    reply_markup=get_currency_choice_keyboard(i18n, currency_id)
                )
            else:
                # Для других языков сразу переходим к вводу значения в USD
                await state.set_state(AlertStates.waiting_for_threshold)
                await state.update_data(currency_id=currency_id, in_rub=False)
                
                await edit_or_send_message(
                    callback.message,
                    i18n.get("alerts-enter-threshold-usd"),
                    reply_markup=back_to_menu_button(i18n)
                )
    except Exception as e:
        logger.error(f"Error in start_set_threshold: {str(e)}", exc_info=True)
        await edit_or_send_message(
            callback.message,
            i18n.get("alerts-error"),
            reply_markup=back_to_menu_button(i18n)
        )

@alerts_router.callback_query(F.data.startswith("alert_set_percent_"))
async def start_set_percent(callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner):
    """Начинает процесс установки процента изменения."""
    try:
        logger.info("Entering start_set_percent handler")
        currency_id = int(callback.data.split("_")[3])
        
        await edit_or_send_message(
            callback.message,
            i18n.get("alerts-choose-percent-type"),
            reply_markup=get_percent_type_keyboard(i18n, currency_id)
        )
    except Exception as e:
        logger.error(f"Error in start_set_percent: {str(e)}", exc_info=True)
        await edit_or_send_message(
            callback.message,
            i18n.get("alerts-error"),
            reply_markup=back_to_menu_button(i18n)
        )

@alerts_router.callback_query(lambda c: c.data.startswith("alert_percent_type_"))
async def process_percent_type(callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner):
    """Обрабатывает выбор типа процентного изменения."""
    try:
        logger.info("Entering process_percent_type handler")
        parts = callback.data.split("_")
        percent_type = parts[3]  # up, down, both
        currency_id = int(parts[4])
        
        await state.set_state(AlertStates.waiting_for_percent)
        await state.update_data(currency_id=currency_id, percent_type=percent_type)
        
        # Показываем сообщение для ввода процента
        type_text = {
            "up": i18n.get("alerts-percent-type-up-text"),
            "down": i18n.get("alerts-percent-type-down-text"),
            "both": i18n.get("alerts-percent-type-both-text")
        }.get(percent_type, "")
        
        await edit_or_send_message(
            callback.message,
            i18n.get("alerts-enter-percent-with-type", type=type_text),
            reply_markup=back_to_menu_button(i18n)
        )
    except Exception as e:
        logger.error(f"Error in process_percent_type: {str(e)}", exc_info=True)
        await edit_or_send_message(
            callback.message,
            i18n.get("alerts-error"),
            reply_markup=back_to_menu_button(i18n)
        )

@alerts_router.message(AlertStates.waiting_for_threshold)
async def process_threshold(message: Message, state: FSMContext, i18n: TranslatorRunner):
    """Обрабатывает введенное пороговое значение."""
    try:
        logger.info("Entering process_threshold handler")
        threshold = float(message.text.replace(",", "").strip())
        data = await state.get_data()
        currency_id = data["currency_id"]
        in_rub = data.get("in_rub", False)
        
        async with get_db() as session:
            currency = await get_user_currency_by_id(session, currency_id)
            alert = await get_alert_settings(session, currency_id)
            
            if alert:
                await update_alert(session, alert.id, threshold=threshold, in_rub=in_rub)
            else:
                alert = await add_alert(session, currency_id, threshold, "threshold", in_rub)
            
            await session.commit()
            await state.clear()
            
            # Показываем сообщение об успехе
            message_key = "alerts-threshold-set-rub" if in_rub else "alerts-threshold-set-usd"
            await message.answer(i18n.get(message_key, value=f"{threshold:.2f}"))
            
            # Создаем фейковый callback для показа настроек
            callback = CallbackQuery(
                id="1",
                from_user=message.from_user,
                chat_instance="1",
                message=message,
                data=f"alert_currency_{currency_id}"
            )
            await show_currency_alerts(callback, i18n)
            
    except ValueError:
        logger.error(f"Invalid threshold value: {message.text}")
        await message.answer(
            i18n.get("alerts-invalid-number"),
            reply_markup=back_to_menu_button(i18n)
        )

@alerts_router.message(AlertStates.waiting_for_percent)
async def process_percent(message: Message, state: FSMContext, i18n: TranslatorRunner):
    """Обрабатывает введенный процент изменения."""
    try:
        logger.info("Entering process_percent handler")
        percent = float(message.text.replace(",", "").strip())
        if percent <= 0:
            raise ValueError("Процент должен быть положительным числом")
            
        data = await state.get_data()
        currency_id = data["currency_id"]
        percent_type = data.get("percent_type", "both")  # по умолчанию both
        
        async with get_db() as session:
            currency = await get_user_currency_by_id(session, currency_id)
            alert = await get_alert_settings(session, currency_id)
            
            if alert:
                await update_alert(session, alert.id, percent_change=percent, percent_type=percent_type)
            else:
                alert = await add_alert(session, currency_id, percent, "percent", percent_type=percent_type)
            
            await session.commit()
            await state.clear()
            
            # Показываем сообщение об успехе с учетом типа
            type_text = {
                "up": i18n.get("alerts-percent-type-up-text"),
                "down": i18n.get("alerts-percent-type-down-text"),
                "both": i18n.get("alerts-percent-type-both-text")
            }.get(percent_type, "")
            
            await message.answer(
                i18n.get("alerts-percent-set-with-type", value=percent, type=type_text)
            )
            
            # Создаем фейковый callback для показа настроек
            callback = CallbackQuery(
                id="1",
                from_user=message.from_user,
                chat_instance="1",
                message=message,
                data=f"alert_currency_{currency_id}"
            )
            await show_currency_alerts(callback, i18n)
            
    except ValueError:
        logger.error(f"Invalid percent value: {message.text}")
        await message.answer(
            i18n.get("alerts-invalid-number"),
            reply_markup=back_to_menu_button(i18n)
        )