# the charging rule
import logging
from django.db import models
from api.models import UuidAuditedModel

logger = logging.getLogger(__name__)


class Rule(UuidAuditedModel):
    """
    the fee rules
    """
    calc_units = (
        (1, 'cpu'),
        (2, 'mem'),
        (3, 'network'),
    )
    name = models.CharField(max_length=64, unique=True)
    calc_unit = models.IntegerField(choices=calc_units)
