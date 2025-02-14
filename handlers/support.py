import logging
from aiogram import Router, F, types
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from fluentogram import TranslatorRunner
from keyboards.inline import back_to_menu_button
from utils.dialog_manager import deactivate_previous_dialogs, register_message

logger = logging.getLogger(__name__)

support_router = Router()


async def show_support(message_or_callback, i18n: TranslatorRunner):
    """Выводит раздел поддержки."""
    user_id = message_or_callback.from_user.id
    logger.info(f"Support command received from user {user_id}")

    try:
        text = i18n.get("cmd-support-text")
        
        if isinstance(message_or_callback, Message):
            await deactivate_previous_dialogs(message_or_callback.chat.id, message_or_callback.bot)
            sent_message = await message_or_callback.answer(text, reply_markup=back_to_menu_button(i18n))
            register_message(message_or_callback.chat.id, sent_message.message_id)
        elif isinstance(message_or_callback, CallbackQuery):
            if message_or_callback.message.reply_markup:
                await message_or_callback.message.edit_text(text, reply_markup=back_to_menu_button(i18n))
                register_message(message_or_callback.message.chat.id, message_or_callback.message.message_id)
            else:
                await deactivate_previous_dialogs(message_or_callback.message.chat.id, message_or_callback.message.bot)
                sent_message = await message_or_callback.message.answer(text, reply_markup=back_to_menu_button(i18n))
                register_message(message_or_callback.message.chat.id, sent_message.message_id)

    except Exception as e:
        logger.error(f"Error in support command for user {user_id}: {str(e)}")

@support_router.message(Command("support"))
async def support_command(message: Message, i18n: TranslatorRunner):
    """Обработчик команды /support."""
    await show_support(message, i18n)

@support_router.callback_query(F.data == "support")
async def support_callback(callback: CallbackQuery, i18n: TranslatorRunner):
    """Обработчик кнопки 'Поддержка'."""
    await show_support(callback, i18n)