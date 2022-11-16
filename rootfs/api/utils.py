"""
Helper functions used by the Drycc Manager server.
"""
from builtins import globals
import os
import logging
import datetime
import redis
import time
import uuid
import hashlib
import pkgutil
import inspect
import random
import string
import calendar
import math
import decimal
from django.db import models
from django.utils import timezone
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.conf import settings

logger = logging.getLogger(__name__)


def invoice_day(): return timezone.now().day if timezone.now().day < 29 else 28


# In order to comply with the Django specification, all models need to be imported
def import_all_models():
    for _, modname, ispkg in pkgutil.iter_modules([
        os.path.join(os.path.dirname(__file__), "models")
    ]):
        if not ispkg:
            mod = __import__(f"api.models.{modname}")
            for subname in dir(mod):
                attr = getattr(mod, subname)
                if inspect.isclass(attr) and issubclass(attr, models.Model):
                    globals()[subname] = attr


def generate_secret(k=64):
    return ''.join(random.choices(string.ascii_letters, k=k))


def get_user_by_name(username):
    return cache.get_or_set(f'user_{username}',
                            lambda: _get_user(username),
                            5 * 60)


def _get_user(username):
    User = get_user_model()
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise
    return user


def platform_credit_to_euro_cent(price):
    """
    1000 platform credit = 1 euro cert
    """
    return math.floor(decimal.Decimal(price) / decimal.Decimal(1000))


def euro_cent_to_platform_credit(price):
    """
    1 euro cert = 1000 platform credit
    """
    return price * 1000


def next_month(t: datetime.datetime) -> datetime.datetime:
    days = calendar.monthrange(t.year, t.month)[1]
    date = t.replace(day=days) + datetime.timedelta(days=1)
    days = calendar.monthrange(date.year, date.month)[1]
    if t.day < days:
        days = t.day
    return t.replace(day=days).replace(year=date.year).replace(month=date.month)


def last_month(t: datetime.datetime) -> datetime.datetime:
    date = t.replace(day=1) - datetime.timedelta(days=1)
    days = calendar.monthrange(date.year, date.month)[1]
    if t.day < days:
        days = t.day
    return t.replace(day=days).replace(year=date.year).replace(month=date.month)


def date2timestamp(date):
    if not isinstance(date, datetime.date):
        raise
    return time.mktime(date.timetuple())


def datetime2timestamp(dt):
    if not isinstance(dt, datetime.datetime):
        raise
    return dt.timestamp()


def timestamp2datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).replace(
        tzinfo=timezone.get_current_timezone()
    )


def strtpime2timestamp(date_string, fmt="%Y%m%d%H"):
    return datetime.datetime.strptime(date_string, fmt).replace(
                tzinfo=timezone.get_current_timezone()).timestamp()


class RedisLock(object):

    WAIT_DELAY = 0.01

    def __init__(self, name, **kwargs):
        self.key = name
        self.value = uuid.uuid4().hex
        self.ttl = kwargs.pop("ttl", 3600)
        self.redis = self.connect(name)

        self._acquire_lock = self.redis.register_script("""
            local key = KEYS[1]
            local value = ARGV[1]
            local ttl = ARGV[2]
            local current_value = redis.call('GET', key)
            if current_value == value or current_value == false then
                redis.call('PSETEX', key, ttl, value)
                return 1
            end
            return 0
        """)
        self._release = self.redis.register_script("""
            local key = KEYS[1]
            local value = ARGV[1]
            if redis.call("GET", key) == value then
                return redis.call("DEL", key)
            else
                return 0
            end
        """)
        self.locked = False
        self.expiration = None

    @staticmethod
    def connect(name):
        md5 = hashlib.md5()
        md5.update(name.encode("utf8"))
        index = int.from_bytes(md5.digest(), byteorder="little") % len(settings.DRYCC_REDIS_ADDRS)
        host, port = settings.DRYCC_REDIS_ADDRS[index].split(":")
        return redis.StrictRedis(
            host=host,
            port=port,
            db=0,
            password=settings.DRYCC_REDIS_PASSWORD
        )

    def __enter__(self):
        self.acquire(blocking=True)
        return self

    def __exit__(self, cls, value, traceback):
        self.release()

    def acquire(self, blocking=False):
        expiration = time.time() + self.ttl
        self.locked = bool(
            self._acquire_lock(keys=[self.key], args=[self.value, int(self.ttl * 1000)])
        )
        if self.locked:
            self.expiration = expiration
        if blocking:
            self.wait()
        return self.locked

    def release(self):
        return bool(self._release(keys=[self.key], args=[self.value]))

    def renew(self):
        return self.acquire(blocking=False)

    def wait(self):
        while not self.locked:
            time.sleep(self._time_to_expire + RedisLock.WAIT_DELAY)
            self.locked = self.acquire()
        return True

    @property
    def _time_to_expire(self):
        return float(self.redis.pttl(self.key) or 0) / 1000


if __name__ == "__main__":
    import doctest

    doctest.testmod()
