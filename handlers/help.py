import logging
from aiogram import Router, F, types
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from fluentogram import TranslatorRunner
from keyboards.inline import back_to_menu_button 

# Настраиваем логгер
logger = logging.getLogger(__name__)

help_router = Router()


async def show_help(message_or_callback, i18n: TranslatorRunner):
    """Выводит раздел помощи."""
    user_id = message_or_callback.from_user.id
    logger.info(f"Help command received from user {user_id}")

    try:
        text = "\n\n".join([
            i18n.get('help-text'),
            i18n.get('help-how-to-use'),
            f"{i18n.get('help-get-rates')}\n{i18n.get('help-get-rates-desc')}",
            f"{i18n.get('help-add-currency')}\n{i18n.get('help-add-currency-desc')}",
            f"{i18n.get('help-set-alert')}\n{i18n.get('help-set-alert-desc')}",
            f"{i18n.get('help-manage-subscription')}\n{i18n.get('help-manage-subscription-desc')}",
            i18n.get('help-commands'),
            i18n.get('help-commands-list'),
            i18n.get('help-support'),
        ])
        
        logger.info(f"Help text generated successfully for user {user_id}")

        if isinstance(message_or_callback, Message):
            await message_or_callback.answer(text, reply_markup=back_to_menu_button(i18n))
        elif isinstance(message_or_callback, CallbackQuery):
            await message_or_callback.message.edit_text(text, reply_markup=back_to_menu_button(i18n))

        logger.info(f"Help message sent to user {user_id}")

    except Exception as e:
        logger.error(f"Error in help command for user {user_id}: {str(e)}")

@help_router.message(Command("help"))
async def help_command(message: Message, i18n: TranslatorRunner):
    """Обработчик команды /help."""
    await show_help(message, i18n)

@help_router.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery, i18n: TranslatorRunner):
    """Обработчик кнопки 'Помощь'."""
    await show_help(callback, i18n)
    