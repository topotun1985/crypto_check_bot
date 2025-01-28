import aiohttp
import logging
from typing import Optional
from config import BINANCE_API_URL, AVAILABLE_CRYPTOCURRENCIES

logger = logging.getLogger(__name__)

class CryptoService:
    def __init__(self):
        self.binance_url = f"{BINANCE_API_URL}/ticker/price"

    async def get_binance_price(self, symbol: str) -> Optional[float]:
        """Получает цену криптовалюты с Binance"""
        try:
            pair = symbol.upper() + "USDT"
            async with aiohttp.ClientSession() as session:
                async with session.get(self.binance_url, params={"symbol": pair}) as response:
                    if response.status == 200:
                        data = await response.json()
                        return float(data["price"])
                    logger.error(f"Ошибка Binance: {response.status}")
        except Exception as e:
            logger.error(f"Ошибка получения цены {symbol}: {e}")
        return None