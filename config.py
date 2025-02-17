import os


TELEGRAM_ALERTS_CHANNEL_ID=-1002266901682
TELEGRAM_ADMIN_ID=855277058


# Доступные криптовалюты
AVAILABLE_CRYPTOCURRENCIES = [
    "BTC", "ETH", "TON", "NOT", "DOGE", "CATI", "XRP", "SOL", "BNB", "MATIC",
    "ADA", "TRX", "AVAX", "SUI", "LINK", "DOT", "BCH", "LTC", "WBETH", "RNDR",
    "ICP", "UNI", "THETA", "XLM", "AAVE", "ATOM", "APT", "ARB", "OM", "TRUMP",
]

# Имена криптовалют для отображения
CRYPTO_NAMES = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "TON": "Toncoin",
    "NOT": "Notcoin",
    "DOGE": "Dogecoin",
    "CATI": "CatCoin",
    "XRP": "Ripple",
    "SOL": "Solana",
    "BNB": "Binance Coin",
    "ADA": "Cardano",
    "TRX": "TRON",
    "AVAX": "Avalanche",
    "SUI": "Sui Network",
    "LINK": "Chainlink",
    "DOT": "Polkadot",
    "BCH": "Bitcoin Cash",
    "LTC": "Litecoin",
    "WBETH": "Wrapped Beacon ETH",
    "RNDR": "Render Token",
    "ICP": "Internet Computer",
    "UNI": "Uniswap",
    "THETA": "Theta Network",
    "XLM": "Stellar",
    "AAVE": "Aave",
    "ATOM": "Cosmos",
    "APT": "Aptos",
    "ARB": "Arbitrum",
    "OM": "MANTRA",
    "TRUMP": "OFFICIAL TRUMP",
    "MATIC": "Polygon"
}



# Настройки Redis
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# Команды бота
BOT_COMMANDS = [
    ("start", "cmd-start"),
    ("help", "cmd-help"),
    ("subscription", "cmd-subscription"),
    ("subscription_terms", "cmd-subscription-terms"), 
    ("support", "cmd-support")
]

# Настройки NATS
NATS_URL = os.getenv("NATS_URL", "nats://nats:4222")

# Настройки Binance API
BINANCE_API_URL = "https://api.binance.com/api/v3"
BINANCE_TICKER_URL = f"{BINANCE_API_URL}/ticker/price"

# Настройки CoinMarketCap API
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY", "")
COINMARKETCAP_API_URL = "https://pro-api.coinmarketcap.com/v1"
