# -*- coding: utf-8 -*-

"""
Data models for the Drycc Manager API.
"""
import logging
import re
import uuid

from django.db import models
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
import requests
from requests_toolbelt import user_agent

from api import __version__ as drycc_version


logger = logging.getLogger(__name__)

session = None


def get_session():
    global session
    if session is None:
        session = requests.Session()
        session.headers = {
            # https://toolbelt.readthedocs.org/en/latest/user-agent.html#user-agent-constructor
            'User-Agent': user_agent('Drycc manager', drycc_version),
        }
        # `mount` a custom adapter that retries failed connections for HTTP and HTTPS requests.
        # http://docs.python-requests.org/en/latest/api/#requests.adapters.HTTPAdapter
        session.mount('http://', requests.adapters.HTTPAdapter(max_retries=10))
        session.mount('https://', requests.adapters.HTTPAdapter(max_retries=10))
    return session


def validate_label(value):
    """
    Check that the value follows the kubernetes name constraints
    http://kubernetes.io/v1.1/docs/design/identifiers.html
    """
    match = re.match(r'^[a-z0-9-]+$', value)
    if not match:
        raise ValidationError("Can only contain a-z (lowercase), 0-9 and hyphens")  # noqa


class AuditedModel(models.Model):
    """Add created and updated fields to a model."""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Mark :class:`AuditedModel` as abstract."""
        abstract = True


class UuidAuditedModel(AuditedModel):
    """Add a UUID primary key to an :class:`AuditedModel`."""

    uuid = models.UUIDField('UUID',
                            default=uuid.uuid4,
                            primary_key=True,
                            editable=False,
                            auto_created=True,
                            unique=True)

    class Meta:
        """Mark :class:`UuidAuditedModel` as abstract."""
        abstract = True


from .bills import Bill  # noqa
from .charge_rules import ChargeRule  # noqa
from .clusters import Cluster  # noqa
from .funding import Funding  # noqa
from .measurement import Config  # noqa
from .measurement import Volume  # noqa
from .measurement import Network  # noqa
from .measurement import Instance  # noqa
from .measurement import Resource  # noqa
from .notifications import Message  # noqa