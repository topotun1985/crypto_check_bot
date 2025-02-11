import asyncio
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
import logging

# Добавляем родительскую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.sharding import ShardManager
from database.models import User, UserCurrency, Alert, Base

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Параметры подключения
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "Vadim22021985")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

async def migrate_data():
    """Миграция данных из основной базы в шарды"""
    try:
        # Подключаемся к основной базе данных
        source_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/crypto_bot"
        source_engine = create_async_engine(source_url)

        # Инициализируем менеджер шардов
        shard_manager = ShardManager()

        # Получаем все данные из основной базы
        async with source_engine.begin() as conn:
            # Получаем всех пользователей
            result = await conn.execute(text("SELECT * FROM users"))
            users = result.fetchall()
            
            logger.info(f"Found {len(users)} users to migrate")

            # Для каждого пользователя
            for user in users:
                # Определяем шард
                shard_id = shard_manager.get_shard_key(user.telegram_id)
                logger.info(f"Migrating user {user.telegram_id} to shard {shard_id}")

                # Получаем движок для шарда
                shard_engine = await shard_manager.get_engine(shard_id)
                if not shard_engine:
                    logger.error(f"Failed to get engine for shard {shard_id}")
                    continue

                async with shard_engine.begin() as shard_conn:
                    # Мигрируем пользователя
                    await shard_conn.execute(
                        text("""
                            INSERT INTO users (id, telegram_id, username, language, created_at, updated_at)
                            VALUES (:id, :telegram_id, :username, :language, :created_at, :updated_at)
                            ON CONFLICT (telegram_id) DO NOTHING
                        """),
                        {
                            "id": user.id,
                            "telegram_id": user.telegram_id,
                            "username": user.username,
                            "language": user.language,
                            "created_at": user.created_at,
                            "updated_at": user.updated_at
                        }
                    )

                    # Получаем валюты пользователя
                    result = await conn.execute(
                        text("SELECT * FROM user_currencies WHERE user_id = :user_id"),
                        {"user_id": user.id}
                    )
                    currencies = result.fetchall()

                    # Мигрируем валюты
                    for currency in currencies:
                        await shard_conn.execute(
                            text("""
                                INSERT INTO user_currencies (id, user_id, currency, created_at, updated_at)
                                VALUES (:id, :user_id, :currency, :created_at, :updated_at)
                                ON CONFLICT (user_id, currency) DO NOTHING
                            """),
                            {
                                "id": currency.id,
                                "user_id": currency.user_id,
                                "currency": currency.currency,
                                "created_at": currency.created_at,
                                "updated_at": currency.updated_at
                            }
                        )

                    # Получаем алерты пользователя
                    result = await conn.execute(
                        text("SELECT * FROM alerts WHERE user_id = :user_id"),
                        {"user_id": user.id}
                    )
                    alerts = result.fetchall()

                    # Мигрируем алерты
                    for alert in alerts:
                        await shard_conn.execute(
                            text("""
                                INSERT INTO alerts (
                                    id, user_id, user_currency_id, threshold,
                                    condition_type, currency_type, is_active,
                                    created_at, updated_at, last_triggered_at
                                )
                                VALUES (
                                    :id, :user_id, :user_currency_id, :threshold,
                                    :condition_type, :currency_type, :is_active,
                                    :created_at, :updated_at, :last_triggered_at
                                )
                                ON CONFLICT (user_id, user_currency_id, condition_type, currency_type) DO NOTHING
                            """),
                            {
                                "id": alert.id,
                                "user_id": alert.user_id,
                                "user_currency_id": alert.user_currency_id,
                                "threshold": alert.threshold,
                                "condition_type": alert.condition_type,
                                "currency_type": alert.currency_type,
                                "is_active": alert.is_active,
                                "created_at": alert.created_at,
                                "updated_at": alert.updated_at,
                                "last_triggered_at": alert.last_triggered_at
                            }
                        )

        logger.info("Data migration completed successfully")

    except Exception as e:
        logger.error(f"Error during migration: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(migrate_data())
