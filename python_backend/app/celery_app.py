from celery import Celery
import os
import redis.connection

# Monkeypatch redis-py Connection class to force RESP2 protocol (protocol=2)
# and disable maintenance notifications to support Redis 5.x.
original_init = redis.connection.Connection.__init__
def patched_init(self, *args, **kwargs):
    kwargs['protocol'] = 2
    kwargs['maint_notifications_config'] = None
    original_init(self, *args, **kwargs)
redis.connection.Connection.__init__ = patched_init

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
    broker_connection_retry_on_startup=True
)
