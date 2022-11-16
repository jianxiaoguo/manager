import uuid
from django.core import signals
from django.contrib.auth import get_user_model
from celery import shared_task
from api.utils import date2timestamp
from api.drycc import DryccClient
from api.models.cluster import Cluster
from api.models.bill import Bill, Invoice
from api.models.charge import ChargeUser
from api.utils import RedisLock

User = get_user_model()


@shared_task(
    autoretry_for=(Exception, ),
    retry_backoff=8,
    retry_jitter=True,
    retry_backoff_max=3600,
    retry_kwargs={'max_retries': 3}
)
def block_user(owner_id):
    task_id = uuid.uuid4().hex
    signals.request_started.send(sender=task_id)
    try:
        for cluster in Cluster.objects.all():
            client = DryccClient(cluster.token)
            response = client.post(
                '{}/v2/manager/{}/{}/block/'.format(cluster.url, "users", owner_id),
                data={'remark': 'Arrears blockade'}
            )
            assert response.status_code == 201
        User.objects.filter(pk=owner_id).update(status=0)
    except Exception as e:
        signals.got_request_exception.send(sender=task_id)
        raise e
    else:
        signals.request_finished.send(sender=task_id)


@shared_task(
    autoretry_for=(Exception, ),
    retry_backoff=8,
    retry_jitter=True,
    retry_backoff_max=3600,
    retry_kwargs={'max_retries': 3}
)
def unblock_user(owner_id):
    task_id = uuid.uuid4().hex
    signals.request_started.send(sender=task_id)
    try:
        for cluster in Cluster.objects.all():
            client = DryccClient(cluster.token)
            response = client.delete(
                '{}/v2/manager/{}/{}/unblock/'.format(cluster.url, "users", owner_id),
            )
            assert response.status_code == 204
        User.objects.filter(pk=owner_id).update(status=1)
    except Exception as e:
        signals.got_request_exception.send(sender=task_id)
        raise e
    else:
        signals.request_finished.send(sender=task_id)


@shared_task(
    autoretry_for=(Exception, ),
    retry_backoff=8,
    retry_jitter=True,
    retry_backoff_max=3600,
    retry_kwargs={'max_retries': 3}
)
def generate_bill(owner_id, bill_date):
    task_id = uuid.uuid4().hex
    signals.request_started.send(sender=task_id)
    try:
        period = int(date2timestamp(bill_date))
        with RedisLock("generate_bill:%s:%s" % (owner_id, period), ttl=600):
            Bill.bulk_create(owner_id, period)
    except Exception as e:
        signals.got_request_exception.send(sender=task_id)
        raise e
    else:
        signals.request_finished.send(sender=task_id)


@shared_task(
    autoretry_for=(Exception, ),
    retry_backoff=8,
    retry_jitter=True,
    retry_backoff_max=3600,
    retry_kwargs={'max_retries': 3}
)
def generate_invoice(owner_id, invoice_date):
    task_id = uuid.uuid4().hex
    signals.request_started.send(sender=task_id)
    try:
        period = int(date2timestamp(invoice_date))
        with RedisLock("generate_invoice:%s:%s" % (owner_id, period), ttl=600):
            invoice = Invoice.create(owner_id, period)
            paying_by_invoice.delay(invoice)
    except Exception as e:
        signals.got_request_exception.send(sender=task_id)
        raise e
    else:
        signals.request_finished.send(sender=task_id)


@shared_task(
    autoretry_for=(Exception, ),
    retry_backoff=8,
    retry_jitter=True,
    retry_backoff_max=3600,
    retry_kwargs={'max_retries': 3}
)
def paying_by_invoice(invoice, arrears_handle=block_user.delay):
    task_id = uuid.uuid4().hex
    signals.request_started.send(sender=task_id)
    with RedisLock("paying_by_invoice:%s" % invoice.owner_id, ttl=600):
        try:
            if not invoice.pay() and arrears_handle:
                arrears_handle(invoice.owner_id)
        except Exception as e:
            signals.got_request_exception.send(sender=task_id)
            raise e
        else:
            signals.request_finished.send(sender=task_id)


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=8,
    retry_jitter=True,
    retry_backoff_max=3600,
    retry_kwargs={'max_retries': 3}
)
def supplementary_payment(owner_id):
    with RedisLock("supplementary_payment:%s" % owner_id, ttl=600):
        for invoice in Invoice.objects.filter(owner_id=owner_id, status=1):
            paying_by_invoice(invoice, arrears_handle=None)
        if not Invoice.objects.filter(owner_id=owner_id, status=1).exists():
            unblock_user.delay(owner_id)


@shared_task(
    autoretry_for=(Exception, ),
    retry_backoff=8,
    retry_jitter=True,
    retry_backoff_max=3600,
    retry_kwargs={'max_retries': 3}
)
def generate_charge_user(day, owner_id):
    task_id = uuid.uuid4().hex
    signals.request_started.send(sender=task_id)
    try:
        ChargeUser.get_or_create(day, owner_id)
    except Exception as e:
        signals.got_request_exception.send(sender=task_id)
        raise e
    else:
        signals.request_finished.send(sender=task_id)
