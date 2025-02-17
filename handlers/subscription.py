import logging
from aiogram import Router, types, F, Bot
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
from keyboards.inline import subscription_menu, main_menu_button, back_to_menu_button
from datetime import datetime, timedelta
from fluentogram import TranslatorRunner
from utils.dialog_manager import deactivate_previous_dialogs, register_message
from .start import back_to_menu, get_subscription_info  # Для правильной навигации

subscription_router = Router()

SUBSCRIPTION_PLANS = {
    "basic": {"limit": 4, "price": 1}, 
    "standard": {"limit": 7, "price": 1}, 
    "premium": {"limit": 10, "price": 1}, 
}

logger = logging.getLogger(__name__)


@subscription_router.callback_query(F.data == "subscription_terms")
async def subscription_terms_callback(callback: CallbackQuery, i18n: TranslatorRunner):
    """Обработчик кнопки 'Условия подписок'"""
    await show_subscription_terms(callback, i18n)
    await callback.answer()


async def show_subscription_menu(message_or_callback, i18n: TranslatorRunner):
    """Отображает текущее состояние подписки и предлагает покупку."""
    user_id = message_or_callback.from_user.id
    try:
        
        async with get_db(telegram_id=message_or_callback.from_user.id) as session:
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

            text = "".join([
                f"{i18n.get('subscription-info', plan=plan.capitalize(), expires=expires_text)}\n\n",
                f"{expires_message}\n\n",
                f"{i18n.get('subscription-currencies', current=currency_count, max=currency_limit)}\n\n",
                f"{i18n.get('subscription-plans')}\n\n",
                f"{i18n.get('plan-basic-description', limit=4)}\n",
                f"{i18n.get('plan-standard-description', limit=7)}\n",
                f"{i18n.get('plan-premium-description', limit=10)}\n\n",
                i18n.get('subscription-validity-period'),
                "\n\n",
                i18n.get('subscription-terms-link')
            ])

            if isinstance(message_or_callback, Message):
                # Команда - создаем новое сообщение
                await deactivate_previous_dialogs(message_or_callback.chat.id, message_or_callback.bot)
                sent_message = await message_or_callback.answer(text, reply_markup=subscription_menu(i18n))
                register_message(message_or_callback.chat.id, sent_message.message_id)
            elif isinstance(message_or_callback, CallbackQuery):
                if message_or_callback.message.reply_markup:
                    # Из меню - редактируем
                    await message_or_callback.message.edit_text(text, reply_markup=subscription_menu(i18n))
                    register_message(message_or_callback.message.chat.id, message_or_callback.message.message_id)
                else:
                    # Отдельная кнопка - новое сообщение
                    await deactivate_previous_dialogs(message_or_callback.message.chat.id, message_or_callback.message.bot)
                    sent_message = await message_or_callback.message.answer(text, reply_markup=subscription_menu(i18n))
                    register_message(message_or_callback.message.chat.id, sent_message.message_id)
    except Exception as e:
        logger.error(f"Error in show_subscription_menu for user {user_id}: {str(e)}")

@subscription_router.message(Command("subscription"))
async def subscription_command(message: Message, i18n: TranslatorRunner):
    """Обработчик команды /subscription."""
    await show_subscription_menu(message, i18n)

@subscription_router.callback_query(F.data == "subscription")
async def subscription_callback(callback: CallbackQuery, i18n: TranslatorRunner):
    """Обработчик кнопки 'Подписка'."""
    await show_subscription_menu(callback, i18n)


@subscription_router.callback_query(F.data == "back_to_subscription")
async def back_to_subscription(callback: CallbackQuery, i18n: TranslatorRunner):
    """Обработчик кнопки возврата в главное меню из invoice"""
    try:
        # Деактивируем все предыдущие диалоги
        bot = callback.message.bot
        chat_id = callback.message.chat.id
        await deactivate_previous_dialogs(chat_id, bot)
        
        # Удаляем сообщение с invoice
        await callback.message.delete()
        
        # Создаем новое сообщение главного меню
        async with get_db(telegram_id=callback.from_user.id) as session:
            subscription_plan, expires_message, currency_count, currency_limit = await get_subscription_info(
                session, callback.from_user.id, i18n
            )

            messages = [
                i18n.get('subscription-info', plan=subscription_plan.capitalize()),
                expires_message,
                i18n.get('subscription-currencies', current=currency_count, max=currency_limit),
                i18n.get('select-action')
            ]
            
            keyboard = main_menu_button(i18n)
            sent_message = await callback.message.answer(text="\n\n".join(messages), reply_markup=keyboard)
            
            # Регистрируем новое сообщение
            register_message(callback.message.chat.id, sent_message.message_id)
            
    except Exception as e:
        logger.error(f"Error in back_to_subscription: {e}")
        await callback.answer(i18n.get("error-occurred"), show_alert=True)


@subscription_router.callback_query(lambda c: c.data.startswith("buy_"))
async def process_buy_subscription(callback: CallbackQuery, i18n: TranslatorRunner):
    """Обрабатывает нажатие на кнопку покупки тарифа через Telegram Stars"""
    plan = callback.data.split("_")[1]  # basic, standard, premium
    user_id = callback.from_user.id
    async with get_db(telegram_id=callback.from_user.id) as session:
        subscription = await get_user_subscription(session, user_id)
        now = datetime.utcnow()

        # Если у пользователя уже есть активная подписка (не free и не истекла), блокируем покупку
        if subscription and subscription.plan != "free" and (not subscription.expires_at or subscription.expires_at > now):
            await callback.answer(
                i18n.get('subscription-already-active', 
                         plan=subscription.plan.capitalize(), 
                         expires=subscription.expires_at.strftime('%d.%m.%Y')),
                show_alert=True
            )
            return  # Выходим из функции, не отправляем invoice

    # Если подписка не активна — продолжаем оформление
    price = SUBSCRIPTION_PLANS[plan]["price"]
    prices = [LabeledPrice(
        label=i18n.get('subscription-price-label', plan=plan.capitalize()),amount=price
    )]

    # Деактивируем предыдущие диалоги перед отправкой invoice
    await deactivate_previous_dialogs(callback.message)

    # Создаем клавиатуру с кнопкой оплаты и кнопкой назад
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text=i18n.get('subscription-payment-button', price=price),
            pay=True
        )],
        [types.InlineKeyboardButton(
            text=i18n.get("btn-back"),
            callback_data="back_to_subscription"
        )]
    ])

    # Отправляем invoice и сохраняем ID сообщения
    invoice_message = await callback.message.answer_invoice(
        title=i18n.get('subscription-invoice-title', plan=plan.capitalize()),
        description=i18n.get('subscription-invoice-description', plan=plan.capitalize()),
        payload=f"subscription_{plan}",
        provider_token="",
        currency="XTR",
        prices=prices,
        reply_markup=keyboard
    )
    
    # Сохраняем ID сообщения с invoice в регистре активных диалогов
    register_message(callback.message.chat.id, invoice_message.message_id)


@subscription_router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery, i18n: TranslatorRunner):
    """Подтверждает оплату"""
    try:
        await pre_checkout_query.answer(ok=True)
    except Exception as e:
        logging.error(f"Pre-checkout error: {e}")
        await pre_checkout_query.answer(
            ok=False,
            error_message=i18n.get("alerts-error")
        )


@subscription_router.message(Command("subscription_terms"))
async def subscription_terms_command(message: Message, i18n: TranslatorRunner):
    """Обработчик команды /subscription_terms"""
    await show_subscription_terms(message, i18n)

async def show_subscription_terms(message_or_callback, i18n: TranslatorRunner):
    """Показывает условия подписок"""
    try:
        
        # Получаем текст с лимитами из конфигурации
        terms_text = i18n.get('subscription-terms-text', 
                            basic_limit=SUBSCRIPTION_PLANS['basic']['limit'],
                            standard_limit=SUBSCRIPTION_PLANS['standard']['limit'],
                            premium_limit=SUBSCRIPTION_PLANS['premium']['limit'])

        # Отправляем сообщение с условиями и кнопкой назад
        if isinstance(message_or_callback, Message):
            # Команда - создаем новое сообщение
            await deactivate_previous_dialogs(message_or_callback.chat.id, message_or_callback.bot)
            msg = await message_or_callback.answer(terms_text, reply_markup=back_to_menu_button(i18n))
            register_message(message_or_callback.chat.id, msg.message_id)
        elif isinstance(message_or_callback, CallbackQuery):
            if message_or_callback.message.reply_markup:
                # Из меню - редактируем
                msg = await message_or_callback.message.edit_text(terms_text, reply_markup=back_to_menu_button(i18n))
                register_message(message_or_callback.message.chat.id, msg.message_id)
            else:
                # Отдельная кнопка - новое сообщение
                await deactivate_previous_dialogs(message_or_callback.message.chat.id, message_or_callback.message.bot)
                msg = await message_or_callback.message.answer(terms_text, reply_markup=back_to_menu_button(i18n))
                register_message(message_or_callback.message.chat.id, msg.message_id)

    except Exception as e:
        logger.error(f"Error showing subscription terms: {e}")
        if isinstance(message_or_callback, Message):
            await message_or_callback.answer(i18n.get("error-occurred"))
        else:
            await message_or_callback.message.edit_text(i18n.get("error-occurred"))


@subscription_router.message(F.successful_payment)
async def process_successful_payment(message: Message, i18n: TranslatorRunner):
    """Обработка успешного платежа"""
    try:
        # Деактивируем предыдущие диалоги
        await deactivate_previous_dialogs(message)
        
        async with get_db(telegram_id=message.from_user.id) as session:
            # Проверяем существование пользователя
            user = await get_user(session, message.from_user.id)
            if not user:
                await add_user(session, message.from_user.id, message.from_user.username)
                
            # Определяем тип подписки из payment_payload
            plan = message.successful_payment.invoice_payload.replace('subscription_', '')
            user_id = message.from_user.id
            
            # Устанавливаем срок действия подписки (1 день)
            expires_at = datetime.utcnow() + timedelta(days=30)
            
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
                i18n.get('subscription-info', plan=subscription_plan.capitalize()),
                i18n.get('subscription-currencies', current=currency_count, max=currency_limit),
                expires_message,
                i18n.get('select-action')
            ]
            
            # Возвращаемся в главное меню с обновленной информацией
            keyboard = main_menu_button(i18n)
            sent_message = await message.answer(text="\n\n".join(messages), reply_markup=keyboard)
            register_message(message.chat.id, sent_message.message_id)
            
    except Exception as e:
        logger.error(f"Error in process_successful_payment for user {message.from_user.id}: {str(e)}")
        await message.answer(i18n.get('alerts-error'))
