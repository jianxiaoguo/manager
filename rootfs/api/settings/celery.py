import os
from celery import Celery, platforms


class Config:
    # Celery Configuration Options
    timezone = "Asia/Shanghai"
    enable_utc = True
    task_serializer = 'pickle'
    accept_content = frozenset([
        'application/data',
        'application/text',
        'application/json',
        'application/x-python-serialize',
    ])
    task_track_started = True
    task_time_limit = 30 * 60
    worker_max_tasks_per_child = 200
    result_expires = 24 * 60 * 60
    broker_url = os.environ.get('DRYCC_RABBITMQ_URL', 'amqp://guest:guest@127.0.0.1:5672/')  # noqa
    cache_backend = 'django-cache'
    task_routes = {
        'api.tasks.generate_bill': {'queue': 'priority.low'},
        'api.tasks.paying_by_bill': {'queue': 'priority.low'},
        'api.tasks.block_user': {'queue': 'priority.middle'},
        'api.tasks.unblock_user': {'queue': 'priority.middle'},
        'api.tasks.supplementary_payment': {'queue': 'priority.high'},
        'api.tasks.generate_charge_user': {'queue': 'priority.high'},
    }
    task_default_queue = 'priority.low'
    worker_cancel_long_running_tasks_on_connection_loss = True


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings.production')
app = Celery('drycc')
app.config_from_object(Config)
app.autodiscover_tasks()
platforms.C_FORCE_ROOT = True
