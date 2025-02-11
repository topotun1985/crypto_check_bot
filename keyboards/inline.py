from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from fluentogram import TranslatorRunner
from config import CRYPTO_NAMES
from database.models import Alert


def main_menu_button(i18n: TranslatorRunner):
    """Главное меню"""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=i18n.get("btn-all-rates"), callback_data="show_all_currency")
    keyboard.button(text=i18n.get("btn-my-currencies"), callback_data="show_my_currencies")
    keyboard.button(text=i18n.get("btn-choose-currency"), callback_data="choose_currency")
    keyboard.button(text=i18n.get("btn-set-alert"), callback_data="notification_settings")
    keyboard.button(text=i18n.get("btn-subscription"), callback_data="subscription")
    keyboard.button(text=i18n.get("btn-help"), callback_data="help")
    keyboard.adjust(1)
    return keyboard.as_markup()


def subscription_menu(i18n: TranslatorRunner):
    """Меню подписки с выбором тарифов"""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=f"{i18n.get('btn-basic')} - {i18n.get('price-star', price=1)}", callback_data="buy_basic")
    keyboard.button(text=f"{i18n.get('btn-standard')} - {i18n.get('price-star', price=1)}", callback_data="buy_standard")
    keyboard.button(text=f"{i18n.get('btn-premium')} - {i18n.get('price-star', price=1)}", callback_data="buy_premium")
    keyboard.button(text=f"{i18n.get('btn-back')}", callback_data="back_to_menu")
    keyboard.adjust(1)
    return keyboard.as_markup()


def back_to_menu_button(i18n: TranslatorRunner):
    """Кнопка назад в главное меню"""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=f"{i18n.get('btn-back')}", callback_data="back_to_menu")
    return keyboard.as_markup()


def get_rates_keyboard(i18n: TranslatorRunner, show_in_rub: bool) -> InlineKeyboardMarkup:
    """Создает клавиатуру с кнопками переключения валюты и возврата в меню."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=i18n.get('btn-toggle-currency',
                             currency=i18n.get('show-in-usd' if show_in_rub else 'show-in-rub')),
                callback_data=f"toggle_currency_display_{'usd' if show_in_rub else 'rub'}"
            )
        ],
        [
            InlineKeyboardButton(
                text=i18n.get('btn-back'),
                callback_data="back_to_menu"
            )
        ]
    ])
    return keyboard


def get_my_currencies_keyboard(i18n: TranslatorRunner, show_in_rub: bool) -> InlineKeyboardMarkup:
    """Клавиатура для раздела 'Мои валюты'."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=i18n.get('btn-toggle-currency',
                             currency=i18n.get('show-in-usd' if show_in_rub else 'show-in-rub')),
                callback_data=f"toggle_my_currency_display_{'usd' if show_in_rub else 'rub'}"
            )
        ],
        [
            InlineKeyboardButton(
                text=i18n.get('btn-back'),
                callback_data="back_to_menu"
            )
        ]
    ])
    return keyboard


def get_choose_currency_keyboard(i18n: TranslatorRunner, user_currencies: list[str]) -> InlineKeyboardMarkup:
    """Клавиатура для выбора валют."""
    keyboard = InlineKeyboardBuilder()
    
    for crypto in CRYPTO_NAMES.keys():
        is_selected = crypto in user_currencies
        text = f"{'✅' if is_selected else '☑️'} {CRYPTO_NAMES[crypto]}"
        keyboard.button(text=text, callback_data=f"toggle_crypto_{crypto}")
    
    keyboard.button(
        text=i18n.get("btn-set-alert"),
        callback_data="notification_settings"
    )
    keyboard.button(
        text=i18n.get("btn-back"),
        callback_data="back_to_menu"
    )
    
    keyboard.adjust(2)
    return keyboard.as_markup()


def get_notification_keyboard(currencies_with_alerts: dict, i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    """Создает клавиатуру со списком валют для настройки уведомлений."""
    keyboard = InlineKeyboardBuilder()
    
    # Добавляем кнопки для каждой валюты
    for currency_id, data in currencies_with_alerts.items():
        # Добавляем статус уведомлений к названию валюты
        status = "✅" if data['has_alerts'] else "☑️"
        keyboard.button(
            text=f"{data['currency']} {status}",
            callback_data=f"alert_currency_{currency_id}"
        )
    
    # Добавляем кнопку "Назад"
    keyboard.button(
        text=i18n.get("btn-back"),
        callback_data="back_to_menu"
    )
    
    keyboard.adjust(1)  # Располагаем кнопки в один столбец
    return keyboard.as_markup()


def get_currency_settings_keyboard(currency_id: int, has_active_alerts: bool, i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    """Создает клавиатуру для настройки уведомлений конкретной валюты."""
    keyboard = InlineKeyboardBuilder()
    
    # Кнопка включения/выключения уведомлений
    if has_active_alerts:
        keyboard.button(
            text=i18n.get("button-disable-alerts"),
            callback_data=f"disable_alerts_{currency_id}"
        )
    else:
        keyboard.button(
            text=i18n.get("button-enable-alerts"),
            callback_data=f"enable_alerts_{currency_id}"
        )
    
    # Кнопки установки порогов
    keyboard.button(
        text=i18n.get("button-set-threshold-above"),
        callback_data=f"set_threshold_above_{currency_id}"
    )
    keyboard.button(
        text=i18n.get("button-set-threshold-below"),
        callback_data=f"set_threshold_below_{currency_id}"
    )
    
    # Кнопка возврата
    keyboard.button(
        text=i18n.get("btn-back"),
        callback_data="back_to_notifications"
    )
    
    keyboard.adjust(1)
    return keyboard.as_markup()


def get_currency_type_keyboard(i18n: TranslatorRunner, currency_id: int, condition_type: str) -> InlineKeyboardMarkup:
    """Создает клавиатуру для выбора типа валюты (USD/RUB)."""
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(
        text=i18n.get("btn-usd"),
        callback_data=f"currency_type_{currency_id}_{condition_type}_usd"
    )
    keyboard.button(
        text=i18n.get("btn-rub"),
        callback_data=f"currency_type_{currency_id}_{condition_type}_rub"
    )
    keyboard.button(
        text=i18n.get("btn-back"),
        callback_data=f"back_to_condition_{currency_id}"
    )
    
    keyboard.adjust(2, 1)
    return keyboard.as_markup()


def get_threshold_input_keyboard(i18n: TranslatorRunner, currency_id: int, condition_type: str, currency_type: str) -> InlineKeyboardMarkup:
    """Создает клавиатуру для ввода порогового значения."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=i18n.get("btn-back"),
        callback_data=f"back_to_currency_type_{currency_id}_{condition_type}"
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


def get_new_alert_keyboard(i18n: TranslatorRunner, alert_id: int, currency_id: int) -> InlineKeyboardMarkup:
    """Создает клавиатуру для установки нового порога после срабатывания уведомления."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=i18n.get("btn-set-new-threshold"),
        callback_data=f"set_new_threshold_{currency_id}_{alert_id}"
    )
    keyboard.button(
        text=i18n.get("btn-back"),
        callback_data=f"alert_currency_{currency_id}"
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


def get_back_to_menu_keyboard(i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    """Создает клавиатуру с кнопкой возврата в главное меню."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=i18n.get("btn-back"),
        callback_data="back_to_menu"
    )
    keyboard.adjust(1)
    return keyboard.as_markup()

