from taskiq_redis import RedisAsyncResultBackend, ListQueueBroker

from app.config import settings

broker = ListQueueBroker(
    url=settings.redis_url,
).with_result_backend(
    RedisAsyncResultBackend(
        redis_url=settings.redis_url,
    ),
)
