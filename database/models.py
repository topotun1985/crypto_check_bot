from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Boolean, DECIMAL, TIMESTAMP, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(70))
    language = Column(String, default="en")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Добавляем связи
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    tracked_currencies = relationship("UserCurrency", back_populates="user")
    alerts = relationship("Alert", back_populates="user")


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    plan = Column(String)
    expires_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Добавляем связь с пользователем
    user = relationship("User", back_populates="subscription")


class UserCurrency(Base):
    __tablename__ = "user_currencies"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    currency = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Добавляем связи
    user = relationship("User", back_populates="tracked_currencies")
    alerts = relationship("Alert", back_populates="user_currency")

    # Добавляем составной уникальный индекс
    __table_args__ = (
        UniqueConstraint('user_id', 'currency', name='uix_user_currency'),
    )


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user_currency_id = Column(Integer, ForeignKey("user_currencies.id", ondelete="CASCADE"))
    threshold = Column(DECIMAL(18,8), nullable=True)  # Сделали необязательным
    percent_change = Column(DECIMAL(5,2), nullable=True)  # Добавили поле для процентного изменения
    percent_type = Column(String, nullable=True)  # up, down, both
    in_rub = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)  # Добавили поле для статуса активности
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Добавляем связи
    user = relationship("User", back_populates="alerts")
    user_currency = relationship("UserCurrency", back_populates="alerts")

    # Добавляем проверку, что хотя бы одно из полей threshold или percent_change должно быть заполнено
    __table_args__ = (
        CheckConstraint('threshold IS NOT NULL OR percent_change IS NOT NULL', 
                       name='check_alert_has_condition'),
    )


class CryptoRate(Base):
    __tablename__ = "crypto_rates"
    id = Column(Integer, primary_key=True)
    currency = Column(String, unique=True, nullable=False)
    price = Column(DECIMAL(18,8), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)


class DollarRate(Base):
    __tablename__ = "dollar_rates"
    id = Column(Integer, primary_key=True, default=1)
    price = Column(DECIMAL(18,8), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    __table_args__ = (
        # Ограничение, чтобы id всегда был 1
        CheckConstraint('id = 1', name='check_id_is_one'),
    )
