import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from fluentogram import TranslatorHub, TranslatorRunner
from dotenv import load_dotenv
from handlers import register_all_handlers
from database.database import create_db_and_tables, get_db
from middlewares.i18n import TranslatorRunnerMiddleware
from utils.i18n import create_translator_hub
from services.tasks import BackgroundTasks
from config import BOT_COMMANDS
from sqlalchemy import select
from database.models import User
from typing import Dict


load_dotenv()

# Настраиваем базовую конфигурацию логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)


def get_commands_for_language(i18n: TranslatorRunner) -> list[BotCommand]:
    """Создает список команд для конкретного языка."""
    return [
        BotCommand(command=command, description=i18n.get(i18n_key))
        for command, i18n_key in BOT_COMMANDS
    ]


async def set_bot_commands(bot: Bot, translator_hub):
    """Устанавливает команды бота для всех языков."""
    # Получаем список всех поддерживаемых языков через поле locale каждого транслятора
    languages = [translator.locale for translator in translator_hub.translators]
    
    # Создаем словарь с командами для каждого языка
    commands_by_language: Dict[str, list[BotCommand]] = {}
    for lang in languages:
        i18n = translator_hub.get_translator_by_locale(locale=lang)
        commands_by_language[lang] = get_commands_for_language(i18n)
    
    # Устанавливаем английские команды как дефолтные
    await bot.set_my_commands(
        commands_by_language["en"],
        scope=BotCommandScopeDefault()
    )
    
    # Устанавливаем команды для пользователей каждого языка
    async with get_db() as session:
        for lang in languages:
            if lang == "en":  # пропускаем английский, так как он уже установлен как дефолтный
                continue
                
            result = await session.execute(
                select(User.telegram_id)
                .where(User.language == lang)
            )
            users = result.scalars().all()
            
            # Устанавливаем команды для каждого пользователя этого языка
            for user_id in users:
                await bot.set_my_commands(
                    commands_by_language[lang],
                    scope=BotCommandScopeChat(chat_id=user_id)
                )

# Функция конфигурирования и запуска бота
async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()

    # Создаем объект типа TranslatorHub
    translator_hub: TranslatorHub = create_translator_hub()

    await create_db_and_tables()

    # Register all handlers
    register_all_handlers(dp)

    # Регистрируем миддлварь для i18n
    dp.update.middleware(TranslatorRunnerMiddleware())

    # Запускаем фоновые задачи
    tasks = BackgroundTasks(bot)
    tasks.i18n = translator_hub.get_translator_by_locale(locale='ru')
    await tasks.start()

    # Регистрируем команды бота
    await set_bot_commands(bot, translator_hub)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, _translator_hub=translator_hub)


if __name__ == "__main__":
    asyncio.run(main())