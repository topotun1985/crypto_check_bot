from math import exp
from fluentogram import TranslatorRunner
from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, Subscription, Alert, UserCurrency, CryptoRate, DollarRate
from datetime import datetime, timezone

# Константы для максимального количества валют по тарифам
SUBSCRIPTION_LIMITS = {
    "free": 1,
    "basic": 5,
    "standard": 10,
    "premium": 20
}

async def add_user(session: AsyncSession, telegram_id: int, username: str, language_code: str = None):
    """Добавляет нового пользователя в базу."""
    new_user = User(
        telegram_id=telegram_id, 
        username=username,
        language=language_code if language_code else "en"
    )
    session.add(new_user)
    await session.commit()
    await add_subscription(session, telegram_id, "free")  

async def get_user(session: AsyncSession, telegram_id: int):
    """Получает пользователя по telegram_id."""
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalars().first()


async def update_user_last_activity(session: AsyncSession, telegram_id: int):
    """Обновляет дату последней активности пользователя."""
    if user := await get_user(session, telegram_id):
        user.updated_at = datetime.utcnow()
        await session.commit()


async def add_subscription(session: AsyncSession, telegram_id: int, plan: str, expires_at: datetime = None, i18n: TranslatorRunner = None):
    """Добавляет или обновляет подписку пользователя."""
    print(f"Adding subscription for user {telegram_id}, plan {plan}")
    
    # Получаем пользователя по telegram_id
    user = await get_user(session, telegram_id)
    if not user:
        raise ValueError(f"User with telegram_id {telegram_id} not found")
        
    subscription = await get_user_subscription(session, telegram_id)
    print(f"Current subscription: {subscription}")

    now = datetime.utcnow()

    # Проверяем, есть ли уже активная подписка (не free и не истекла)
    if subscription and subscription.plan != "free" and (not subscription.expires_at or subscription.expires_at > now):
        return i18n.get(
            'subscription-already-active-db',
            plan=subscription.plan.capitalize(),
            expires=subscription.expires_at.strftime('%d.%m.%Y')
        )
    
    if subscription:
        print(f"Updating existing subscription")
        subscription.plan = plan
        subscription.expires_at = expires_at
    else:
        print(f"Creating new subscription")
        subscription = Subscription(user_id=user.id, plan=plan, expires_at=expires_at)
        session.add(subscription)
    
    try:
        await session.commit()
        print(f"Subscription saved successfully")
    except Exception as e:
        print(f"Error saving subscription: {e}")
        raise
    
    return subscription


async def get_user_subscription(session: AsyncSession, telegram_id: int):
    """Получает подписку пользователя по telegram_id."""
    user = await get_user(session, telegram_id)
    if not user:
        return None
    result = await session.execute(select(Subscription).where(Subscription.user_id == user.id))
    return result.scalars().first()


async def reset_expired_subscriptions(session: AsyncSession):
    """Сбрасывает истекшие подписки и ограничивает валюты для free."""
    now = datetime.now(timezone.utc).replace(tzinfo=None)  # Убираем таймзону

    # Обновляем подписку на free, если она истекла
    stmt = (
        update(Subscription)
        .where(Subscription.expires_at < now)
        .values(plan="free", expires_at=None)
    )
    await session.execute(stmt)

    # Удаляем лишние валюты для пользователей, у которых подписка стала free
    free_limit = SUBSCRIPTION_LIMITS["free"]
    result = await session.execute(
        select(UserCurrency.user_id)
        .join(Subscription, Subscription.user_id == UserCurrency.user_id)
        .where(Subscription.plan == "free")
        .group_by(UserCurrency.user_id)
        .having(func.count(UserCurrency.id) > free_limit)
    )
    users_to_update = result.scalars().all()

    for user_id in users_to_update:
        result = await session.execute(
            select(UserCurrency)
            .where(UserCurrency.user_id == user_id)
            .order_by(UserCurrency.created_at.asc())  
        )
        currencies = result.scalars().all()
        
        # Оставляем только самые старые валюты в пределах лимита
        for currency in currencies[free_limit:]:
            await session.delete(currency)

    await session.commit()


def get_subscription_limit(plan: str) -> int:
    """Возвращает максимальное количество валют для тарифа."""
    return SUBSCRIPTION_LIMITS.get(plan, SUBSCRIPTION_LIMITS["free"])


async def format_subscription_expires(subscription) -> str:
    """Форматирует дату окончания подписки."""
    if not subscription or subscription.plan == "free":
        return "∞"  # или можно использовать перевод
    if not subscription.expires_at:
        return ""
    return subscription.expires_at.strftime('%d.%m.%Y')


async def get_user_currency_count(session: AsyncSession, telegram_id: int) -> int:
    """Получает количество отслеживаемых валют пользователя."""
    user = await get_user(session, telegram_id)
    if not user:
        return 0
        
    result = await session.execute(
        select(func.count(UserCurrency.id))
        .where(UserCurrency.user_id == user.id)
    )
    return result.scalar() or 0


async def get_user_currencies(session: AsyncSession, telegram_id: int) -> list[UserCurrency]:
    """Получает список валют пользователя."""
    user = await get_user(session, telegram_id)
    if not user:
        return []
        
    result = await session.execute(
        select(UserCurrency)
        .where(UserCurrency.user_id == user.id)
    )
    return result.scalars().all()

async def add_user_currency(session: AsyncSession, telegram_id: int, currency: str):
    """Добавляет валюту для отслеживания."""
    user = await get_user(session, telegram_id)
    if not user:
        return
        
    # Проверяем лимит валют
    subscription = await get_user_subscription(session, telegram_id)
    current_currencies = await get_user_currencies(session, telegram_id)
    currency_limit = SUBSCRIPTION_LIMITS.get(subscription.plan if subscription else "free", SUBSCRIPTION_LIMITS["free"])
    
    if len(current_currencies) >= currency_limit:
        raise ValueError("Достигнут лимит валют для вашей подписки")
        
    # Проверяем нет ли уже такой валюты
    existing = await session.execute(
        select(UserCurrency)
        .where(
            UserCurrency.user_id == user.id,
            UserCurrency.currency == currency
        )
    )
    if existing.scalar_one_or_none():
        return
        
    # Добавляем валюту
    currency_obj = UserCurrency(
        user_id=user.id,
        currency=currency
    )
    session.add(currency_obj)
    await session.commit()
    return currency_obj

async def remove_user_currency(session: AsyncSession, telegram_id: int, currency: str):
    """Удаляет валюту из отслеживаемых."""
    user = await get_user(session, telegram_id)
    if not user:
        return
        
    # Удаляем валюту
    await session.execute(
        delete(UserCurrency)
        .where(
            UserCurrency.user_id == user.id,
            UserCurrency.currency == currency
        )
    )
    await session.commit()


async def add_alert(session: AsyncSession, user_id: int, user_currency_id: int, threshold: float, 
                   condition_type: str, currency_type: str):
    """Добавляет или обновляет настройки уведомлений."""
    # Проверяем существующий алерт с такими же параметрами
    result = await session.execute(
        select(Alert).where(
            Alert.user_id == user_id,
            Alert.user_currency_id == user_currency_id,
            Alert.condition_type == condition_type,
            Alert.currency_type == currency_type
        )
    )
    alert = result.scalars().first()
    
    if alert:
        # Обновляем существующий алерт
        alert.threshold = threshold
        alert.is_active = True
    else:
        # Создаем новый алерт
        alert = Alert(
            user_id=user_id,
            user_currency_id=user_currency_id,
            threshold=threshold,
            condition_type=condition_type,
            currency_type=currency_type,
            is_active=True
        )
        session.add(alert)
    
    await session.commit()
    return alert

async def get_alert_settings(session: AsyncSession, user_currency_id: int):
    """Получает настройки уведомлений для валюты пользователя."""
    result = await session.execute(
        select(Alert)
        .where(Alert.user_currency_id == user_currency_id)
    )
    return result.scalar()  # Return first result or None


async def get_all_currency_alerts(session: AsyncSession, user_id: int, user_currency_id: int):
    """Получает все уведомления для валюты пользователя."""
    result = await session.execute(
        select(Alert).where(
            Alert.user_id == user_id,
            Alert.user_currency_id == user_currency_id
        )
    )
    return result.scalars().all()

async def delete_alert(session: AsyncSession, user_id: int, user_currency_id: int):
    """Удаляет все настройки уведомлений для валюты."""
    await session.execute(
        delete(Alert).where(
            Alert.user_id == user_id,
            Alert.user_currency_id == user_currency_id
        )
    )
    await session.commit()

async def update_alert(session: AsyncSession, alert_id: int, is_active: bool = None, threshold: float = None):
    """Обновляет настройки уведомления."""
    result = await session.execute(select(Alert).where(Alert.id == alert_id))
    alert = result.scalar_one_or_none()
    
    if alert:
        if is_active is not None:
            alert.is_active = is_active
        if threshold is not None:
            alert.threshold = threshold
        
        alert.updated_at = datetime.utcnow()
        await session.commit()
    
    return alert

async def get_user_currency_by_id(session: AsyncSession, user_currency_id: int) -> UserCurrency:
    """Получает валюту пользователя по ID."""
    result = await session.execute(
        select(UserCurrency)
        .where(UserCurrency.id == user_currency_id)
    )
    return result.scalar_one_or_none()

async def get_crypto_rate(session: AsyncSession, currency: str) -> CryptoRate:
    """Получает текущий курс криптовалюты."""
    result = await session.execute(
        select(CryptoRate)
        .where(CryptoRate.currency == currency)
    )
    return result.scalar_one_or_none()

async def get_all_crypto_rates(session: AsyncSession):
    """Получает все курсы криптовалют."""
    result = await session.execute(
        select(CryptoRate)
        .order_by(CryptoRate.currency)
    )
    return result.scalars().all()


async def get_dollar_rate(session: AsyncSession):
    """Получает текущий курс доллара."""
    result = await session.execute(
        select(DollarRate)
        .order_by(DollarRate.id.desc())
        .limit(1)
    )
    return result.scalars().first()


async def update_crypto_rate(session: AsyncSession, currency: str, price: float):
    """Обновляет курс криптовалюты."""
    rate = await session.execute(
        select(CryptoRate).where(CryptoRate.currency == currency)
    )
    rate = rate.scalars().first()
    
    if rate:
        rate.price = price
        rate.updated_at = datetime.utcnow()
    else:
        rate = CryptoRate(currency=currency, price=price)
        session.add(rate)
    
    await session.commit()
    return rate


async def update_dollar_rate(session: AsyncSession, price: float):
    """Обновляет курс доллара."""
    result = await session.execute(select(DollarRate).where(DollarRate.id == 1))
    rate = result.scalars().first()
    
    if rate:
        rate.price = price
        rate.updated_at = datetime.utcnow()
    else:
        rate = DollarRate(id=1, price=price)
        session.add(rate)
    
    await session.commit()
    return rate


