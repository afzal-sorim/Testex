# Monkey patch redis.ConnectionPool to force protocol=2 (RESP2) for compatibility with older Redis servers
try:
    import redis
    original_pool_init = redis.ConnectionPool.__init__
    def patched_pool_init(self, *args, **connection_kwargs):
        connection_kwargs['protocol'] = 2
        original_pool_init(self, *args, **connection_kwargs)
    redis.ConnectionPool.__init__ = patched_pool_init
except Exception:
    pass

from celery import Celery
import os

redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "migration_tasks",
    broker=redis_url,
    backend=redis_url,
    include=['app.tasks']
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    broker_connection_retry_on_startup=True,
    broker_transport_options={'protocol': 2}
)
