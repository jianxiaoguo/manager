import os
from kombu import Exchange, Queue
from celery import Celery


class Config(object):
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
    task_default_queue = 'manager.low'
    task_default_exchange = 'manager.priority'
    task_default_routing_key = 'manager.priority.low'
    worker_cancel_long_running_tasks_on_connection_loss = True


app = Celery('drycc')
app.config_from_object(Config())
app.conf.update(
    task_routes={
        'api.tasks.generate_bill': {
            'queue': 'manager.low',
            'exchange': 'manager.priority',
            'routing_key': 'manager.priority.low',
        },
        'api.tasks.paying_by_bill': {
            'queue': 'manager.low',
            'exchange': 'manager.priority',
            'routing_key': 'manager.priority.low',
        },
        'api.tasks.block_user': {
            'queue': 'manager.middle',
            'exchange': 'manager.priority',
            'routing_key': 'manager.priority.middle',
        },
        'api.tasks.unblock_user': {
            'queue': 'manager.middle',
            'exchange': 'manager.priority',
            'routing_key': 'manager.priority.middle',
        },
        'api.tasks.supplementary_payment': {
            'queue': 'manager.high',
            'exchange': 'manager.priority',
            'routing_key': 'manager.priority.high',
        },
        'api.tasks.generate_charge_user': {
            'queue': 'manager.high',
            'exchange': 'manager.priority',
            'routing_key': 'manager.priority.high',
        },
    },
    task_queues=(
        Queue(
            'manager.low',
            exchange=Exchange('manager.priority', type="direct"),
            routing_key='manager.priority.low',
            queue_arguments={'x-max-priority': 16},
        ),
        Queue(
            'manager.high',
            exchange=Exchange('manager.priority', type="direct"),
            routing_key='manager.priority.high',
            queue_arguments={'x-max-priority': 64},
        ),
        Queue(
            'manager.middle',
            exchange=Exchange('manager.priority', type="direct"),
            routing_key='manager.priority.middle',
            queue_arguments={'x-max-priority': 32},
        ),
    ),
)
app.autodiscover_tasks()
