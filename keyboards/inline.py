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
    keyboard.button(text=i18n.get("btn-set-alert"), callback_data="show_alerts")
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
        callback_data="setup_notifications"
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


def get_alert_settings_keyboard(i18n: TranslatorRunner, currency_id: int, alert: Alert = None, language: str = "en") -> InlineKeyboardMarkup:
    """Создает клавиатуру для настройки уведомлений конкретной валюты."""
    keyboard = InlineKeyboardBuilder()
    
    # Кнопка включения/выключения уведомлений
    if alert and alert.is_active:
        keyboard.button(
            text=i18n.get("button-disable-alerts"),
            callback_data=f"alert_toggle_{currency_id}"
        )
    else:
        keyboard.button(
            text=i18n.get("button-enable-alerts"),
            callback_data=f"alert_toggle_{currency_id}"
        )
    
    # Кнопки настройки порогов и процентов
    if language == "ru":
        # Для русского языка показываем одну кнопку для порога
        keyboard.button(
            text=i18n.get("button-change-threshold" if alert and alert.threshold else "button-set-threshold"),
            callback_data=f"alert_set_threshold_{currency_id}"
        )
    else:
        # Для других языков показываем кнопку только для USD
        keyboard.button(
            text=i18n.get("button-set-threshold-usd"),
            callback_data=f"alert_set_threshold_{currency_id}"
        )
    
    keyboard.button(
        text=i18n.get("button-set-percent"),
        callback_data=f"alert_set_percent_{currency_id}"
    )
    
    # Кнопки навигации
    keyboard.button(
        text=i18n.get("button-back-to-alerts"),
        callback_data="show_alerts"
    )
    
    keyboard.adjust(1)  # Располагаем кнопки в один столбец
    return keyboard.as_markup()


def get_currency_choice_keyboard(i18n: TranslatorRunner, currency_id: int) -> InlineKeyboardMarkup:
    """Создает клавиатуру для выбора валюты порога."""
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(
        text=i18n.get("alerts-choose-usd"),
        callback_data=f"alert_currency_choice_usd_{currency_id}"
    )
    
    keyboard.button(
        text=i18n.get("alerts-choose-rub"),
        callback_data=f"alert_currency_choice_rub_{currency_id}"
    )
    
    keyboard.button(
        text=i18n.get("btn-back"),
        callback_data=f"alert_currency_{currency_id}"
    )
    
    keyboard.adjust(1)
    return keyboard.as_markup()


def get_percent_type_keyboard(i18n: TranslatorRunner, currency_id: int) -> InlineKeyboardMarkup:
    """Создает клавиатуру для выбора типа процентного изменения."""
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(
        text=i18n.get("alerts-percent-type-up"),
        callback_data=f"alert_percent_type_up_{currency_id}"
    )
    
    keyboard.button(
        text=i18n.get("alerts-percent-type-down"),
        callback_data=f"alert_percent_type_down_{currency_id}"
    )
    
    keyboard.button(
        text=i18n.get("alerts-percent-type-both"),
        callback_data=f"alert_percent_type_both_{currency_id}"
    )
    
    keyboard.button(
        text=i18n.get("btn-back"),
        callback_data=f"alert_currency_{currency_id}"
    )
    
    keyboard.adjust(1)
    return keyboard.as_markup()
