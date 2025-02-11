from typing import List, Optional, Tuple, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Alert, UserCurrency, User

if TYPE_CHECKING:
    from database.sharding import ShardManager

class AlertRepository:
    def __init__(self, shard_manager: 'ShardManager'):
        self.shard_manager = shard_manager

    async def get_active_alerts_for_shard(self, shard_id: int, session: AsyncSession) -> List[Tuple[Alert, UserCurrency, User]]:
        """Получает все активные алерты для конкретного шарда"""
        result = await session.execute(
            select(Alert, UserCurrency, User)
            .join(UserCurrency, Alert.user_currency_id == UserCurrency.id)
            .join(User, UserCurrency.user_id == User.id)
            .where(Alert.is_active == True)
        )
        return result.all()

    async def update_alert_status(self, 
                                alert: Alert, 
                                is_active: bool, 
                                session: AsyncSession,
                                last_triggered_at: Optional[datetime] = None):
        """Обновляет статус алерта"""
        alert.is_active = is_active
        if last_triggered_at:
            alert.last_triggered_at = last_triggered_at
        alert.updated_at = datetime.utcnow()
        await session.commit()

    async def get_user_alerts(self, user_id: int, currency_id: int, session: AsyncSession) -> List[Alert]:
        """Получает все алерты пользователя для конкретной валюты"""
        result = await session.execute(
            select(Alert)
            .join(UserCurrency, Alert.user_currency_id == UserCurrency.id)
            .where(
                UserCurrency.user_id == user_id,
                UserCurrency.id == currency_id
            )
        )
        return result.scalars().all()

    async def create_alert(self, 
                          user_currency_id: int,
                          threshold: float,
                          condition_type: str,
                          currency_type: str,
                          session: AsyncSession) -> Alert:
        """Создает новый алерт"""
        alert = Alert(
            user_currency_id=user_currency_id,
            threshold=threshold,
            condition_type=condition_type,
            currency_type=currency_type,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(alert)
        await session.commit()
        return alert

    async def update_alert(self,
                          alert_id: int,
                          threshold: float,
                          session: AsyncSession) -> Optional[Alert]:
        """Обновляет порог алерта"""
        result = await session.execute(
            select(Alert).where(Alert.id == alert_id)
        )
        alert = result.scalar_one_or_none()
        if alert:
            alert.threshold = threshold
            alert.updated_at = datetime.utcnow()
            alert.is_active = True
            await session.commit()
        return alert
