import aiohttp
import logging
from typing import Optional
from config import COINMARKETCAP_API_KEY, COINMARKETCAP_API_URL

logger = logging.getLogger(__name__)

class FiatService:
    def __init__(self):
        self.coinmarketcap_url = f"{COINMARKETCAP_API_URL}/tools/price-conversion"
        self.headers = {'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY}

    async def get_usd_rate(self) -> Optional[float]:
        """Получает курс USD → RUB с CoinMarketCap"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.coinmarketcap_url, 
                                       params={"amount": "1", "symbol": "USD", "convert": "RUB"},
                                       headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return float(data["data"]["quote"]["RUB"]["price"])
                    logger.error(f"Ошибка CoinMarketCap: {response.status}")
        except Exception as e:
            logger.error(f"Ошибка получения USD/RUB: {e}")
        return None