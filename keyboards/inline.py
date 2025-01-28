from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner


def main_menu_button(i18n: TranslatorRunner):
    """Главное меню"""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=i18n.get("btn-all-rates"), callback_data="show_all_currency")
    keyboard.button(text=i18n.get("btn-choose-currency"), callback_data="choose_currency")
    keyboard.button(text=i18n.get("btn-set-alert"), callback_data="set_alert")
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
