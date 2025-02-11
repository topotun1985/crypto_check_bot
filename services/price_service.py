import logging
from typing import Optional
from decimal import Decimal

logger = logging.getLogger(__name__)

class PriceService:
    def __init__(self):
        self._prices = {}
        
    async def update_price(self, currency: str, usd_price: Decimal, rub_price: Decimal):
        """Обновление цены для валюты"""
        self._prices[currency] = {
            'USD': usd_price,
            'RUB': rub_price
        }
        
    async def get_price(self, currency: str, currency_type: str) -> Optional[Decimal]:
        """Получение текущей цены валюты"""
        try:
            return self._prices.get(currency, {}).get(currency_type)
        except Exception as e:
            logger.error(f"Error getting price for {currency}: {str(e)}")
            return None

# Создаем глобальный экземпляр сервиса
price_service = PriceService()
