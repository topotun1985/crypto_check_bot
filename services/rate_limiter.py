import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Set
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class RateLimitBucket:
    """Bucket для rate limiting с поддержкой burst"""
    max_tokens: int
    refill_rate: float  # tokens per second
    tokens: float = field(init=False)
    last_update: datetime = field(init=False)
    
    def __post_init__(self):
        self.tokens = float(self.max_tokens)
        self.last_update = datetime.now()
    
    def update(self) -> None:
        now = datetime.now()
        delta = (now - self.last_update).total_seconds()
        self.tokens = min(
            self.max_tokens,
            self.tokens + delta * self.refill_rate
        )
        self.last_update = now
    
    def try_acquire(self, tokens: float = 1.0) -> bool:
        self.update()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

class TelegramRateLimiter:
    """Rate limiter с учетом ограничений Telegram"""
    def __init__(self):
        self.global_bucket = RateLimitBucket(
            max_tokens=28,  # максимум 30 сообщений в секунду
            refill_rate=28.0  # восстанавливаем 30 токенов в секунду
        )
        self.user_buckets: Dict[int, RateLimitBucket] = {}
        self.lock = asyncio.Lock()
        self.delayed_queue: List[tuple] = []  # [(timestamp, user_id, priority), ...]
        self._cleanup_task: Optional[asyncio.Task] = None
        
    async def start(self):
        """Запускает обработчик отложенных сообщений"""
        self._cleanup_task = asyncio.create_task(self._process_delayed_queue())
    
    async def stop(self):
        """Останавливает обработчик"""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
    
    def _get_user_bucket(self, user_id: int) -> RateLimitBucket:
        """Получает или создает bucket для пользователя"""
        if user_id not in self.user_buckets:
            self.user_buckets[user_id] = RateLimitBucket(
                max_tokens=1,  # максимум 1 сообщение в секунду (ограничение Telegram)
                refill_rate=1.0  # восстанавливаем 1 токен в секунду
            )
        return self.user_buckets[user_id]
    
    async def can_send(self, user_id: int, priority: bool = False) -> bool:
        """Проверяет, можно ли отправить сообщение"""
        async with self.lock:
            user_bucket = self._get_user_bucket(user_id)
            if not user_bucket.try_acquire() or not self.global_bucket.try_acquire():
                # Если нельзя отправить сейчас, добавляем в очередь
                delay = 0.5 if priority else 2.0  # Приоритетные сообщения ждут меньше
                scheduled_time = datetime.now() + timedelta(seconds=delay)
                self.delayed_queue.append((scheduled_time, user_id, priority))
                return False
            return True
    
    async def wait_for_slot(self, user_id: int, priority: bool = False):
        """Ожидает, пока не появится возможность отправить сообщение"""
        user_bucket = self._get_user_bucket(user_id)
        if not user_bucket.try_acquire() or not self.global_bucket.try_acquire():
            # Если не можем отправить сейчас, добавляем в очередь
            delay = 1.0  # Строго 1 секунда между сообщениями
            scheduled_time = datetime.now() + timedelta(seconds=delay)
            async with self.lock:
                self.delayed_queue.append((scheduled_time, user_id, priority))
            
            # Ждем, пока сообщение не будет обработано
            while True:
                async with self.lock:
                    if not any(u_id == user_id for _, u_id, _ in self.delayed_queue):
                        break
                await asyncio.sleep(0.1)
            return False
        return True
    
    async def _process_delayed_queue(self):
        """Обрабатывает отложенные сообщения"""
        while True:
            try:
                now = datetime.now()
                next_message = None
                
                async with self.lock:
                    if not self.delayed_queue:
                        await asyncio.sleep(0.1)
                        continue
                        
                    # Сортируем по времени и приоритету
                    self.delayed_queue.sort(key=lambda x: (x[0], not x[2]))
                    
                    # Берем первое сообщение из очереди
                    next_message = self.delayed_queue[0]
                    
                if next_message:
                    scheduled_time, user_id, priority = next_message
                    if scheduled_time <= now:
                        # Проверяем rate limit
                        user_bucket = self._get_user_bucket(user_id)
                        if user_bucket.try_acquire() and self.global_bucket.try_acquire():
                            async with self.lock:
                                if self.delayed_queue and self.delayed_queue[0] == next_message:
                                    # Успешно получили слот для отправки
                                    self.delayed_queue.pop(0)
                                    logger.info(f"Processing message for user {user_id} (priority: {priority})")
                                    # Строго ждем 1 секунду перед следующим сообщением
                                    await asyncio.sleep(1.0)
                        else:
                            # Если не удалось отправить, планируем следующую попытку
                            async with self.lock:
                                if self.delayed_queue and self.delayed_queue[0] == next_message:
                                    new_delay = 1.0  # Строго 1 секунда между сообщениями
                                    self.delayed_queue[0] = (now + timedelta(seconds=new_delay), user_id, priority)
                                    logger.debug(f"Rescheduling message for user {user_id} in {new_delay} seconds")
                                    await asyncio.sleep(0.1)
                
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"Error processing delayed queue: {e}")
                await asyncio.sleep(1.0)
