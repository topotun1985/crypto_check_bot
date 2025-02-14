from .start import start_router
from .help import help_router
from .subscription import subscription_router
from .rates import rates_router
from .my_currencies import my_currencies_router
from .choose_currency import choose_currency_router
from .notification_settings import notification_router
from .unsupported import unsupported_router 
from .support import support_router

def register_all_handlers(dp):
    """Register all handlers."""
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(subscription_router)
    dp.include_router(rates_router)
    dp.include_router(my_currencies_router)
    dp.include_router(choose_currency_router)
    dp.include_router(notification_router)
    dp.include_router(support_router)
    dp.include_router(unsupported_router)  # Добавляем последним, чтобы он ловил все оставшиеся сообщения

__all__ = [
    'register_all_handlers',
    'start_router',
    'help_router',
    'support_router',
    'subscription_router',
    'rates_router',
    'my_currencies_router',
    'choose_currency_router',
    'notification_router'
]
