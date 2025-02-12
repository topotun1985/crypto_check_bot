import os
import asyncio
import logging
import signal
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
from services.notification_service import NotificationService


from config import BOT_COMMANDS
from sqlalchemy import select
from database.models import User
from typing import Dict
from contextlib import suppress


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
    # Создаем объекты для хранения сервисов
    bot = None
    notification_service = None
    tasks = None
    
    # Функция для корректного завершения работы
    async def shutdown(signal_type=None):
        nonlocal bot, notification_service, tasks
        
        logger.info(f'Received signal {signal_type}, shutting down...')
        
        # Останавливаем фоновые задачи
        if tasks:
            tasks.is_running = False
            logger.info('Background tasks stopped')
        
        # Закрываем соединение с NATS
        if notification_service:
            with suppress(Exception):
                await notification_service.close()
                logger.info('NATS connection closed')
        
        # Закрываем сессию бота
        if bot:
            with suppress(Exception):
                await bot.session.close()
                logger.info('Bot session closed')
        
        # Останавливаем event loop
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        [task.cancel() for task in tasks]
        logger.info(f'Cancelling {len(tasks)} outstanding tasks')
        await asyncio.gather(*tasks, return_exceptions=True)
        asyncio.get_event_loop().stop()
        logger.info('Shutdown complete')
    
    try:
        # Инициализируем бота
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
        
        # Добавляем translator_hub в данные диспетчера
        dp.workflow_data.update({"_translator_hub": translator_hub})
        
        # Создаем сервисы
        notification_service = NotificationService(
            bot=bot,
            translator_hub=translator_hub,
            nats_url=os.getenv("NATS_URL", "nats://nats:4222")
        )
        # Запускаем фоновые задачи
        tasks = BackgroundTasks(
            bot=bot,
            notification_service=notification_service
        )
        tasks.i18n = translator_hub.get_translator_by_locale(locale='ru')
        
        # Подключаемся к NATS
        try:
            await notification_service.connect()
            logger.info("Successfully connected to NATS")
        except Exception as e:
            logger.error(f"Failed to connect to NATS: {e}")
            raise
        
        await tasks.start()
        
        # TODO: Временно отключаем установку команд
        # await set_bot_commands(bot, translator_hub)
        
        # Устанавливаем обработчики сигналов
        for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGABRT):
            asyncio.get_event_loop().add_signal_handler(
                sig,
                lambda s=sig: asyncio.create_task(shutdown(s))
            )
        
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, _translator_hub=translator_hub)
        
    except Exception as e:
        logger.error(f"Critical error: {e}", exc_info=True)
        await shutdown()
        raise
    finally:
        await shutdown()


if __name__ == "__main__":
    asyncio.run(main())