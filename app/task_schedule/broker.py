from taskiq_redis import RedisStreamBroker, RedisAsyncResultBackend
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

from app.core import config


redis_url = config.redis.url

result_backend = RedisAsyncResultBackend(redis_url=redis_url)
broker = RedisStreamBroker(url=redis_url).with_result_backend(result_backend)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)
