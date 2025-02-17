from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import time
import logging
import psutil
import multiprocessing
import asyncio
from monitoring.prometheus_metrics import ERROR_COUNTER, CPU_USAGE
from monitoring.decorators import track_request_latency
from config import TELEGRAM_ALERTS_CHANNEL_ID

def cpu_intensive_task():
    """Задача, которая нагружает CPU"""
    start = time.time()
    while time.time() - start < 120:  # Работаем 2 минуты
        # Более интенсивные вычисления
        for _ in range(1000000):
            _ = 2 ** 16


logger = logging.getLogger(__name__)

router = Router()

async def is_admin(message: Message) -> bool:
    """Проверяет, является ли пользователь администратором"""
    return message.from_user.id == TELEGRAM_ADMIN_ID

@router.message(Command("test_errors"))
@track_request_latency(handler_name="test_errors")
async def test_errors(message: Message):
    if not await is_admin(message):
        await message.answer("❌ Эта команда доступна только администратору")
        return
    """Тестирование алерта HighErrorRate"""
    try:
        logger.info("Starting error test...")
        for i in range(100):
            ERROR_COUNTER.labels(error_type="test", shard="main").inc()
            if i % 20 == 0:
                logger.info(f"Generated {i} errors...")
        logger.info("Error test completed")
        await message.answer("Сгенерировано 100 ошибок для проверки алерта HighErrorRate")
    except Exception as e:
        logger.error(f"Error in test_errors: {e}")
        await message.answer(f"Ошибка при генерации ошибок: {e}")

@router.message(Command("test_cpu"))
@track_request_latency(handler_name="test_cpu")
async def test_cpu(message: Message):
    if not await is_admin(message):
        await message.answer("❌ Эта команда доступна только администратору")
        return
    """Тестирование алерта HighCPUUsage"""
    processes = []
    try:
        logger.info("Starting CPU test...")
        await message.answer("Начинаю нагрузку CPU на 120 секунд...")
        
        # Запускаем несколько процессов для нагрузки CPU
        num_processes = multiprocessing.cpu_count()  # Используем все доступные ядра
        
        for _ in range(num_processes):
            p = multiprocessing.Process(target=cpu_intensive_task)
            p.start()
            processes.append(p)
        
        # Мониторим нагрузку
        start = time.time()
        while time.time() - start < 120:
            if int(time.time() - start) % 10 == 0:
                logger.info(f"CPU test running for {int(time.time() - start)} seconds...")
            await asyncio.sleep(1)
        
        logger.info("CPU test completed")
        await message.answer("Тест CPU нагрузки завершен")
    except Exception as e:
        logger.error(f"Error in test_cpu: {e}")
        await message.answer(f"Ошибка при тесте CPU: {e}")
    finally:
        # Гарантируем остановку всех процессов
        for p in processes:
            try:
                p.terminate()
                p.join(timeout=1)
            except Exception as e:
                logger.error(f"Error stopping process: {e}")

@router.message(Command("test_channel"))
async def test_channel(message: Message):
    if not await is_admin(message):
        await message.answer("❌ Эта команда доступна только администратору")
        return
    """Тестирование отправки в канал"""
    try:
        await message.bot.send_message(
            chat_id=TELEGRAM_ALERTS_CHANNEL_ID,
            text="🔵 *Тестовое сообщение*\n\n```\nПроверка работы алертов\n```",
            parse_mode="Markdown"
        )
        await message.answer("Тестовое сообщение отправлено в канал")
    except Exception as e:
        await message.answer(f"Ошибка при отправке: {e}")

@router.message(Command("check_metrics"))
async def check_metrics(message: Message):
    """Проверка текущих значений метрик"""
    try:
        from prometheus_client import REGISTRY

        # Получаем текущие значения метрик
        error_metrics = [m for m in REGISTRY.collect() if m.name == 'bot_errors_total']
        cpu_metrics = [m for m in REGISTRY.collect() if m.name == 'bot_cpu_usage_percent']

        # Формируем отчет
        report = [
            "📈 *Текущие значения метрик:*",
            "```"
        ]

        # Добавляем CPU метрики
        if cpu_metrics:
            for sample in cpu_metrics[0].samples:
                report.append(f"CPU Usage: {sample.value}%")
        else:
            report.append("CPU Usage: Not available")

        # Добавляем метрики ошибок
        report.append("\nErrors:")
        if error_metrics:
            for sample in error_metrics[0].samples:
                labels = ', '.join(f"{k}={v}" for k, v in sample.labels.items())
                report.append(f"- [{labels}]: {sample.value}")
        else:
            report.append("- No errors recorded")
        
        report.append("```")
        
        # Отправляем отчет
        await message.answer("\n".join(report), parse_mode="Markdown")
        logger.info(f"Metrics checked: {len(error_metrics)} error metrics, {len(cpu_metrics)} CPU metrics")
    except Exception as e:
        error_msg = f"Ошибка при проверке метрик: {e}"
        logger.error(error_msg)
        await message.answer(error_msg)
