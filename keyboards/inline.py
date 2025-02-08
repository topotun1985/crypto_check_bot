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


def get_alerts_list_keyboard(i18n: TranslatorRunner, currency_alerts: list) -> InlineKeyboardMarkup:
    """Создает клавиатуру со списком валют для настройки уведомлений."""
    keyboard = InlineKeyboardBuilder()
    
    # Добавляем кнопки для каждой валюты
    for currency, alert in currency_alerts:
        # Добавляем статус уведомлений к названию валюты
        status = "✅" if alert and alert.is_active else "☑️"
        keyboard.button(
            text=f"{currency.currency} {status}",
            callback_data=f"alert_currency_{currency.id}"
        )
    
    # Добавляем кнопку "Назад"
    keyboard.button(
        text=i18n.get("btn-back"),
        callback_data="back_to_menu"
    )
    
    keyboard.adjust(1)  # Располагаем кнопки в один столбец
    return keyboard.as_markup()


def get_alert_settings_keyboard(i18n: TranslatorRunner, currency_id: int, alerts: list[Alert] = None, user_language: str = None) -> InlineKeyboardMarkup:
    """Создает клавиатуру для настройки уведомлений конкретной валюты."""
    keyboard = InlineKeyboardBuilder()
    
    # Проверяем есть ли активные алерты
    has_active_alerts = any(alert.is_active for alert in alerts) if alerts else False
    
    # Кнопка включения/выключения уведомлений
    if has_active_alerts:
        keyboard.button(
            text=i18n.get("button-disable-alerts"),
            callback_data=f"disable_alert_{alerts[0].id}"
        )
    else:
        keyboard.button(
            text=i18n.get("button-enable-alerts"),
            callback_data=f"enable_alerts_{currency_id}"
        )
    
    # Кнопки настройки порогов в USD
    keyboard.button(
        text=i18n.get("button-set-threshold-above"),
        callback_data=f"alert_set_threshold_{currency_id}_above_usd"
    )
    keyboard.button(
        text=i18n.get("button-set-threshold-below"),
        callback_data=f"alert_set_threshold_{currency_id}_below_usd"
    )
    
    # Если пользователь русскоязычный, добавляем кнопки для RUB
    if user_language == "ru":
        keyboard.button(
            text=i18n.get("button-set-threshold-above-rub"),
            callback_data=f"alert_set_threshold_{currency_id}_above_rub"
        )
        keyboard.button(
            text=i18n.get("button-set-threshold-below-rub"),
            callback_data=f"alert_set_threshold_{currency_id}_below_rub"
        )
        keyboard.adjust(1, 2, 2)  # 1 кнопка в первой строке, по 2 в остальных
    else:
        keyboard.adjust(1, 2)  # 1 кнопка в первой строке, 2 во второй
    
    # Кнопка возврата к списку валют
    keyboard.button(
        text=i18n.get("btn-back"),
        callback_data="back_to_notifications"
    )
    keyboard.adjust(1)
    
    return keyboard.as_markup()


def get_currency_choice_keyboard(i18n: TranslatorRunner, currency_id: int, condition_type: str = "above") -> InlineKeyboardMarkup:
    """Создает клавиатуру для выбора валюты порога."""
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(
        text=i18n.get("button-choose-usd"),
        callback_data=f"alert_currency_usd_{currency_id}_{condition_type}"
    )
    keyboard.button(
        text=i18n.get("button-choose-rub"),
        callback_data=f"alert_currency_rub_{currency_id}_{condition_type}"
    )
    
    keyboard.button(
        text=i18n.get("btn-back"),
        callback_data=f"alert_currency_{currency_id}"
    )
    
    keyboard.adjust(1)
    return keyboard.as_markup()


def get_currency_type_keyboard(i18n: TranslatorRunner, currency_id: int, condition_type: str) -> InlineKeyboardMarkup:
    """Создает клавиатуру для выбора типа валюты (USD/RUB)."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=i18n.get("button-set-threshold-usd"),
        callback_data=f"set_currency_type_{currency_id}_{condition_type}_usd"
    )
    keyboard.button(
        text=i18n.get("button-set-threshold-rub"),
        callback_data=f"set_currency_type_{currency_id}_{condition_type}_rub"
    )
    keyboard.button(
        text=i18n.get("btn-back"),
        callback_data=f"set_threshold_{currency_id}_{condition_type}"
    )
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_threshold_input_keyboard(i18n: TranslatorRunner, currency_id: int, condition_type: str, currency_type: str) -> InlineKeyboardMarkup:
    """Создает клавиатуру для ввода порогового значения."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=i18n.get("btn-back"),
        callback_data="back_to_condition"
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


def get_new_alert_keyboard(i18n: TranslatorRunner, alert_id: int, currency: str) -> InlineKeyboardMarkup:
    """Создает клавиатуру для установки нового порога после срабатывания уведомления."""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=i18n.get("btn-set-new-threshold"),
        callback_data=f"set_new_threshold_{alert_id}"
    )
    keyboard.adjust(1)
    return keyboard.as_markup()
