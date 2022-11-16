import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from api.utils import invoice_day


def get_anonymous_user_instance(user): return user(id=-1)


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


class User(AbstractUser):
    STATUS_CHOICES = [
        (0, 'block'),
        (1, 'normal'),
    ]
    id = models.BigIntegerField(_('id'), primary_key=True)
    email = models.EmailField(_('email address'), unique=True)
    status = models.PositiveSmallIntegerField(
        _('status'), db_index=True, choices=STATUS_CHOICES, default=STATUS_CHOICES[1][0])
    invoice_day = models.PositiveSmallIntegerField(_('invoice day'), default=invoice_day)
