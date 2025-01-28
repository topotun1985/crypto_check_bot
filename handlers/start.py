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

async def get_subscription_info(session: AsyncSession, user_id: int, i18n: TranslatorRunner) -> tuple[str, str, int, int]:
    """Получает информацию о подписке пользователя."""
    subscription = await get_user_subscription(session, user_id)
    subscription_plan = subscription.plan if subscription else "free"
    expires_text = await format_subscription_expires(subscription)
    
    if subscription and subscription.plan != "free":
        expires_message = i18n.get('subscription-expires-until', expires=expires_text)
    else:
        expires_message = i18n.get('subscription-expires-infinite')
    
    currency_count = await get_user_currency_count(session, user_id)
    currency_limit = get_subscription_limit(subscription_plan)
    
    return subscription_plan, expires_message, currency_count, currency_limit


@start_router.message(Command("start"))
async def start_command(message: Message, i18n: TranslatorRunner):
    async with get_db() as session:
        user = await get_user(session, message.from_user.id)
        username = message.from_user.full_name

        if not user:
            await add_user(session, message.from_user.id, username)
            await session.commit()  

        subscription_plan, expires_message, currency_count, currency_limit = await get_subscription_info(
            session, message.from_user.id, i18n
        )

        messages = [
            i18n.get('hello-user', username=username),
            i18n.get('subscription-info', plan=subscription_plan),
            expires_message,
            i18n.get('subscription-currencies', current=currency_count, max=currency_limit),
            i18n.get('welcome-text')
        ]

        keyboard = main_menu_button(i18n)
        await message.answer(text="\n\n".join(messages), reply_markup=keyboard)
        await update_user_last_activity(session, message.from_user.id)


@start_router.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, i18n: TranslatorRunner):
    async with get_db() as session:
        subscription_plan, expires_message, currency_count, currency_limit = await get_subscription_info(
            session, callback.from_user.id, i18n
        )

        messages = [
            i18n.get('subscription-info', plan=subscription_plan),
            expires_message,
            i18n.get('subscription-currencies', current=currency_count, max=currency_limit),
            i18n.get('select-action')
        ]
        
        keyboard = main_menu_button(i18n)
        await callback.message.edit_text(text="\n\n".join(messages), reply_markup=keyboard)
