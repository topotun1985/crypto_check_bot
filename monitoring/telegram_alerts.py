from aiogram import Bot
import asyncio
import json
import logging
from aiohttp import web
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TelegramAlerter:
    def __init__(self, bot: Bot, channel_id: str, admin_id: int):
        self.bot = bot
        self.channel_id = channel_id
        self.admin_id = admin_id
        self.app = web.Application()
        self.app.router.add_post('/alert', self.handle_alert)
        self.severity_emoji = {
            'critical': '🔴',
            'warning': '🟡',
            'info': '🔵'
        }

    async def format_alert_message(self, alert: Dict[str, Any]) -> str:
        """Форматирует сообщение алерта для Telegram"""
        severity = alert.get('labels', {}).get('severity', 'info')
        emoji = self.severity_emoji.get(severity, '❓')
        
        message = [
            f"{emoji} *{alert.get('annotations', {}).get('summary', 'Alert')}*",
            f"```",
            f"Severity: {severity}",
            f"Description: {alert.get('annotations', {}).get('description', 'No description')}",
            f"Started: {alert.get('startsAt', 'Unknown')}",
            f"```"
        ]
        
        return "\n".join(message)

    async def send_alert(self, message: str, is_critical: bool = False):
        """Отправляет алерт в канал мониторинга"""
        try:
            logger.info(f"Sending alert to channel {self.channel_id}")
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode="Markdown"
            )
            logger.info(f"Alert sent to channel successfully")
        except Exception as e:
            logger.error(f"Error sending alert: {e}", exc_info=True)

    async def handle_alert(self, request: web.Request) -> web.Response:
        """Обработчик входящих алертов от AlertManager"""
        try:
            data = await request.json()
            logger.info(f"Received alert data: {json.dumps(data, indent=2)}")
            
            for alert in data.get('alerts', []):
                logger.info(f"Processing alert: {json.dumps(alert, indent=2)}")
                message = await self.format_alert_message(alert)
                logger.info(f"Formatted message: {message}")
                is_critical = alert.get('labels', {}).get('severity') == 'critical'
                logger.info(f"Is critical: {is_critical}")
                
                await self.send_alert(message, is_critical)
            
            return web.Response(text='OK', status=200)
        except Exception as e:
            logger.error(f"Error processing alert: {e}", exc_info=True)
            return web.Response(text=str(e), status=500)

    async def start(self, host: str = '0.0.0.0', port: int = 9087):
        """Запускает веб-сервер для приема алертов"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()
        logger.info(f"Alert receiver started on {host}:{port}")
