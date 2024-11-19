import os
from kombu import Exchange, Queue
from celery import Celery


class Config(object):
    # Celery Configuration Options
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
    worker_prefetch_multiplier = 1
    result_expires = 24 * 60 * 60
    cache_backend = 'django-cache'
    task_default_queue = 'manager.middle'
    task_default_exchange = 'manager.priority'
    task_default_routing_key = 'manager.priority.middle'
    broker_transport_options = {"queue_order_strategy": "sorted"}
    task_create_missing_queues = True
    task_inherit_parent_priority = True
    broker_connection_retry_on_startup = True
    worker_cancel_long_running_tasks_on_connection_loss = True


app = Celery('manager')
app.config_from_object(Config())
app.conf.update(
    timezone=os.environ.get('TZ', 'UTC'),
    task_routes={
        'api.tasks.generate_bill': {
            'queue': 'manager.low',
            'exchange': 'manager.priority', 'routing_key': 'manager.priority.low',
        },
        'api.tasks.paying_by_bill': {
            'queue': 'manager.low',
            'exchange': 'manager.priority', 'routing_key': 'manager.priority.low',
        },
        'api.tasks.block_user': {
            'queue': 'manager.middle',
            'exchange': 'manager.priority', 'routing_key': 'manager.priority.middle',
        },
        'api.tasks.unblock_user': {
            'queue': 'manager.middle',
            'exchange': 'manager.priority', 'routing_key': 'manager.priority.middle',
        },
        'api.tasks.supplementary_payment': {
            'queue': 'manager.high',
            'exchange': 'manager.priority', 'routing_key': 'manager.priority.high',
        },
        'api.tasks.generate_charge_user': {
            'queue': 'manager.high',
            'exchange': 'manager.priority', 'routing_key': 'manager.priority.high',
        },
    },
    task_queues=(
        Queue(
            'manager.low', exchange=Exchange('manager.priority', type="direct"),
            routing_key='manager.priority.low',
        ),
        Queue(
            'manager.high', exchange=Exchange('manager.priority', type="direct"),
            routing_key='manager.priority.high',
        ),
        Queue(
            'manager.middle', exchange=Exchange('manager.priority', type="direct"),
            routing_key='manager.priority.middle',
        ),
    ),
)

# SET valkey
DRYCC_VALKEY_URL = os.environ.get('DRYCC_VALKEY_URL', 'redis://:@127.0.0.1:6379')
app.conf.update(
    broker_url=DRYCC_VALKEY_URL,
    result_backend=DRYCC_VALKEY_URL,
    broker_transport_options={"queue_order_strategy": "sorted", "visibility_timeout": 43200},
)
app.autodiscover_tasks()
