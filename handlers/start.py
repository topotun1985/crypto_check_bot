from aiogram import Router, F, types
from aiogram.filters import Command
from database.queries import (
    add_user, get_user, update_user_last_activity, get_user_subscription,
    get_user_currency_count, get_subscription_limit, format_subscription_expires
)
from database.database import get_db
from aiogram.types import Message, CallbackQuery
from keyboards.inline import main_menu_button
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

start_router = Router()

async def get_subscription_info(session: AsyncSession, telegram_id: int, i18n: TranslatorRunner) -> tuple[str, str, int, int]:
    """Получает информацию о подписке пользователя."""
    subscription = await get_user_subscription(session, telegram_id)
    subscription_plan = subscription.plan if subscription else "free"
    expires_text = await format_subscription_expires(subscription)
    
    if subscription and subscription.plan != "free":
        expires_message = i18n.get('subscription-expires-until', expires=expires_text)
    else:
        expires_message = i18n.get('subscription-expires-infinite')
    
    currency_count = await get_user_currency_count(session, telegram_id)
    currency_limit = get_subscription_limit(subscription_plan)
    
    return subscription_plan, expires_message, currency_count, currency_limit


from utils.dialog_manager import deactivate_previous_dialogs, register_message

import logging

logger = logging.getLogger(__name__)

@start_router.message(Command("start"))
async def start_command(message: Message, i18n: TranslatorRunner):
    async with get_db() as session:
        try:
            # Деактивируем предыдущие диалоги до отправки нового сообщения
            await deactivate_previous_dialogs(message)
            
            user = await get_user(session, message.from_user.id)
            username = message.from_user.full_name or i18n.get('default-username')

            if not user:
                await add_user(session, message.from_user.id, username)
                await session.commit()  

            subscription_plan, expires_message, currency_count, currency_limit = await get_subscription_info(
                session, message.from_user.id, i18n
            )

            messages = [
                i18n.get('hello-user', username=username),
                i18n.get('subscription-info', plan=subscription_plan.capitalize()),
                expires_message,
                i18n.get('subscription-currencies', current=currency_count, max=currency_limit),
                i18n.get('welcome-text')
            ]
            
            # Отправляем новое сообщение
            sent_message = await message.answer(
                "\n\n".join(messages),
                reply_markup=main_menu_button(i18n)
            )
            
            # Регистрируем новое сообщение
            register_message(message.chat.id, sent_message.message_id)
            
            # Обновляем время последней активности
            await update_user_last_activity(session, message.from_user.id)
            
        except Exception as e:
            logger.error(f"Error in start_command: {e}")
            # В случае ошибки просто отправляем сообщение
            sent_message = await message.answer(
                "\n\n".join(messages),
                reply_markup=main_menu_button(i18n)
            )
            register_message(message.chat.id, sent_message.message_id)
        await update_user_last_activity(session, message.from_user.id)


@start_router.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, i18n: TranslatorRunner):
    async with get_db() as session:
        try:
            
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
            await callback.message.edit_text(text="\n\n".join(messages), reply_markup=keyboard)
            
            # Регистрируем обновленное сообщение
            register_message(callback.message.chat.id, callback.message.message_id)
            
        except Exception as e:
            logger.error(f"Error in back_to_menu: {e}")
