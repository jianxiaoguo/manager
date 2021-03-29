# -*- coding: utf-8 -*-

"""
Data models for the Drycc Manager API.
"""
import logging
import uuid

from django.db import models

logger = logging.getLogger(__name__)


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
