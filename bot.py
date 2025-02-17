import os
import asyncio
import logging
import signal
import config
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
from monitoring.setup import MonitoringService


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
    """Устанавливает команды бота для каждого поддерживаемого языка."""
    # Список поддерживаемых языков
    supported_languages = ["ru", "en", "de", "es", "fr", "it", "pt"]
    
    try:
        # Удаляем глобальные команды (без языка)
        await bot.delete_my_commands(scope=BotCommandScopeDefault())
        
        # Удаляем команды для каждого языка
        for lang in supported_languages:
            try:
                await bot.delete_my_commands(
                    scope=BotCommandScopeDefault(),
                    language_code=lang
                )
            except Exception as e:
                logger.warning(f"Failed to delete commands for {lang}: {e}")
        
        # Устанавливаем команды для каждого языка
        for lang in supported_languages:
            try:
                # Получаем переводчик для конкретного языка
                i18n = translator_hub.get_translator_by_locale(locale=lang)
                # Получаем локализованные команды
                commands = get_commands_for_language(i18n)
                
                # Устанавливаем команды для конкретного языка
                await bot.set_my_commands(
                    commands,
                    scope=BotCommandScopeDefault(),
                    language_code=lang
                )
                logger.info(f"Set commands for language: {lang}")
            except Exception as e:
                logger.error(f"Failed to set commands for {lang}: {e}")
        
        # Устанавливаем английские команды как дефолтные (без указания языка)
        i18n = translator_hub.get_translator_by_locale(locale="en")
        default_commands = get_commands_for_language(i18n)
        await bot.set_my_commands(default_commands, scope=BotCommandScopeDefault())
        
    except Exception as e:
        logger.error(f"Failed to set bot commands: {e}")

# Функция конфигурирования и запуска бота
async def main():
    # Создаем объекты для хранения сервисов
    bot = None
    notification_service = None
    tasks = None
    monitoring_service = None
    
    # Функция для корректного завершения работы
    async def shutdown(signal_type=None):
        nonlocal bot, notification_service, tasks, monitoring_service
        
        logger.info(f'Received signal {signal_type}, shutting down...')
        
        # Останавливаем фоновые задачи
        if tasks:
            tasks.is_running = False
            logger.info('Background tasks stopped')
            
        # Останавливаем мониторинг
        if monitoring_service:
            await monitoring_service.stop()
            logger.info('Monitoring service stopped')
        
        # Закрываем соединение с NATS и останавливаем rate limiter
        if notification_service:
            with suppress(Exception):
                await notification_service.close()
                await notification_service.rate_limiter.stop()
                logger.info('NATS connection closed and rate limiter stopped')
        
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
        
        # Подключаемся к NATS и запускаем rate limiter
        try:
            await notification_service.connect()
            await notification_service.rate_limiter.start()
            logger.info("Successfully connected to NATS and started rate limiter")
        except Exception as e:
            logger.error(f"Failed to initialize services: {e}")
            raise
        
        await tasks.start()
        
        # Инициализируем и запускаем мониторинг
        monitoring_service = MonitoringService(
            bot=bot,
            prometheus_port=config.MONITORING_PROMETHEUS_PORT,
            alerter_port=config.MONITORING_ALERTER_PORT,
            channel_id=str(config.TELEGRAM_ALERTS_CHANNEL_ID),
            admin_id=config.TELEGRAM_ADMIN_ID
        )
        await monitoring_service.start()
        logger.info("Monitoring service started")

        await set_bot_commands(bot, translator_hub)
        
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