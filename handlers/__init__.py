from aiogram import Router
from .start import start_router
from .help import help_router
from .subscription import subscription_router
from .rates import rates_router
from .my_currencies import my_currencies_router
from .choose_currency import choose_currency_router
from .alerts import alerts_router


def register_all_handlers(dp: Router):
    """Регистрирует все обработчики."""
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(subscription_router)
    dp.include_router(rates_router)
    dp.include_router(my_currencies_router)
    dp.include_router(choose_currency_router)
    dp.include_router(alerts_router)
