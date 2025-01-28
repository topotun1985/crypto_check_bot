import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message
from database.queries import (
                                get_user_subscription, 
                                format_subscription_expires, 
                                get_subscription_limit, 
                                add_subscription, 
                                get_user_currency_count,
                                get_user,
                                add_user
                            )
from database.database import get_db
from keyboards.inline import subscription_menu, main_menu_button
from datetime import datetime, timedelta
from fluentogram import TranslatorRunner

subscription_router = Router()

SUBSCRIPTION_PLANS = {
    "basic": {"limit": 5, "price": 1}, 
    "standart": {"limit": 10, "price": 1}, 
    "premium": {"limit": 20, "price": 1}, 
}

logger = logging.getLogger(__name__)


async def show_subscription_menu(message_or_callback, i18n: TranslatorRunner):
    """Отображает текущее состояние подписки и предлагает покупку."""
    async with get_db() as session:
        user_id = message_or_callback.from_user.id
        subscription = await get_user_subscription(session, user_id)
        plan = subscription.plan if subscription else "free"
        expires_text = await format_subscription_expires(subscription)

        expires_message = (
            i18n.get('subscription-expires-until', expires=expires_text) 
            if subscription and subscription.plan != "free" 
            else i18n.get('subscription-expires-infinite')
        )

        currency_limit = get_subscription_limit(plan)
        currency_count = await get_user_currency_count(session, user_id)

        text = " ".join([
            f"{i18n.get('subscription-info', plan=plan.capitalize(), expires=expires_text)}\n\n",
            f"{expires_message}\n\n",
            f"{i18n.get('subscription-currencies', current=currency_count, max=currency_limit)}\n\n",
            f"{i18n.get('subscription-plans')}\n",
            f"{i18n.get('plan-basic-description', limit=5)}\n",
            f"{i18n.get('plan-standard-description', limit=10)}\n",
            f"{i18n.get('plan-premium-description', limit=20)}\n\n",
            i18n.get('subscription-validity-period')
        ])

        if isinstance(message_or_callback, Message):
            await message_or_callback.answer(text, reply_markup=subscription_menu(i18n))
        elif isinstance(message_or_callback, CallbackQuery):
            await message_or_callback.message.edit_text(text, reply_markup=subscription_menu(i18n))

@subscription_router.message(Command("subscription"))
async def subscription_command(message: Message, i18n: TranslatorRunner):
    """Обработчик команды /subscription."""
    await show_subscription_menu(message, i18n)

@subscription_router.callback_query(F.data == "subscription")
async def subscription_callback(callback: CallbackQuery, i18n: TranslatorRunner):
    """Обработчик кнопки 'Подписка'."""
    await show_subscription_menu(callback, i18n)


@subscription_router.callback_query(lambda c: c.data.startswith("buy_"))
async def process_buy_subscription(callback: CallbackQuery):
    """Обрабатывает нажатие на кнопку покупки тарифа через Telegram Stars"""
    plan = callback.data.split("_")[1]  # basic, advanced, premium
    price = SUBSCRIPTION_PLANS[plan]["price"]

    prices = [LabeledPrice(label=f"Подписка {plan.capitalize()}", amount=price)]

    await callback.message.answer_invoice(
        title=f"{plan.capitalize()} подписка",
        description=f"Оформите подписку {plan.capitalize()} на 30 дней",
        payload=f"subscription_{plan}",
        provider_token="",  # Telegram Stars → оставляем пустым
        currency="XTR",
        prices=prices,
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text=f"Отправить {price} ⭐️", pay=True)]]
        )
    )


@subscription_router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    """Подтверждает оплату"""
    try:
        await pre_checkout_query.answer(ok=True)
    except Exception as e:
        logging.error(f"Pre-checkout error: {e}")
        await pre_checkout_query.answer(
            ok=False,
            error_message="Произошла ошибка. Попробуйте позже."
        )


@subscription_router.message(F.successful_payment)
async def process_successful_payment(message: Message, i18n: TranslatorRunner):
    """Обработка успешного платежа"""
    async with get_db() as session:
        # Проверяем существование пользователя
        user = await get_user(session, message.from_user.id)
        if not user:
            await add_user(session, message.from_user.id, message.from_user.username)
            
        # Определяем тип подписки из payment_payload
        plan = message.successful_payment.invoice_payload.replace('subscription_', '')
        user_id = message.from_user.id
        
        # Устанавливаем срок действия подписки (1 день)
        expires_at = datetime.utcnow() + timedelta(days=1)
        
        # Обновляем подписку в базе
        await add_subscription(session, user_id, plan, expires_at)
        
        # Получаем обновленную информацию о подписке для отображения
        subscription = await get_user_subscription(session, user_id)
        subscription_plan = subscription.plan
        expires_text = await format_subscription_expires(subscription)
        currency_count = await get_user_currency_count(session, user_id)
        currency_limit = get_subscription_limit(subscription_plan)

        if subscription and subscription.plan != "free":
            expires_message = i18n.get('subscription-expires-until', expires=expires_text)
        else:
            expires_message = i18n.get('subscription-expires-infinite')
        
        # Формируем сообщение с обновленной информацией
        messages = [
            i18n.get('subscription-purchase-success'),
            i18n.get('subscription-info', plan=subscription_plan),
            i18n.get('subscription-currencies', current=currency_count, max=currency_limit),
            expires_message,
            i18n.get('select-action')
        ]
        
        # Возвращаемся в главное меню с обновленной информацией
        keyboard = main_menu_button(i18n)
        await message.answer(text="\n\n".join(messages), reply_markup=keyboard)
        
