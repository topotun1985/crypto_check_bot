from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import CommandStart, CommandObject
from fluentogram import TranslatorRunner

unsupported_router = Router()

@unsupported_router.message(F.text & ~F.text.startswith(('/')))
async def handle_text(message: Message, i18n: TranslatorRunner):
    """Обработчик текстовых сообщений, которые не являются командами"""
    await message.reply(i18n.get("unsupported-text-message"))

@unsupported_router.message(F.photo)
async def handle_photo(message: Message, i18n: TranslatorRunner):
    """Обработчик фото"""
    await message.reply(i18n.get("unsupported-photo"))

@unsupported_router.message(F.sticker)
async def handle_sticker(message: Message, i18n: TranslatorRunner):
    """Обработчик стикеров"""
    await message.reply(i18n.get("unsupported-sticker"))

@unsupported_router.message(F.document)
async def handle_document(message: Message, i18n: TranslatorRunner):
    """Обработчик документов"""
    await message.reply(i18n.get("unsupported-document"))

@unsupported_router.message(F.voice)
async def handle_voice(message: Message, i18n: TranslatorRunner):
    """Обработчик голосовых сообщений"""
    await message.reply(i18n.get("unsupported-voice"))

@unsupported_router.message(F.video)
async def handle_video(message: Message, i18n: TranslatorRunner):
    """Обработчик видео"""
    await message.reply(i18n.get("unsupported-video"))

# Этот обработчик будет ловить все остальные типы сообщений
@unsupported_router.message()
async def handle_other(message: Message, i18n: TranslatorRunner):
    """Обработчик всех остальных типов сообщений"""
    await message.reply(i18n.get("unsupported-message"))
