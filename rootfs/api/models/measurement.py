import logging
from django.db import models
from api.models import UuidAuditedModel

logger = logging.getLogger(__name__)


class MeasurementModel(UuidAuditedModel):
    cluster = models.ForeignKey('Cluster', on_delete=models.PROTECT)
    app_id = models.CharField(max_length=63, db_index=True)
    owner_id = models.CharField(max_length=63, db_index=True)
    timestamp = models.FloatField(db_index=True)

    class Meta:
        """Mark :class:`MeasurementModel` as abstract."""
        abstract = True


class Config(MeasurementModel):
    container_type = models.CharField(max_length=63)
    cpu = models.PositiveIntegerField()
    memory = models.PositiveIntegerField()


class Volume(MeasurementModel):
    name = models.CharField(max_length=63)
    size = models.PositiveIntegerField()


class Network(MeasurementModel):
    pod_name = models.CharField(max_length=63)
    rx_bytes = models.PositiveIntegerField()
    tx_bytes = models.PositiveIntegerField()


class Instance(MeasurementModel):
    container_type = models.CharField(max_length=63)
    container_count = models.PositiveIntegerField()


class Resource(MeasurementModel):
    name = models.CharField(max_length=63)
    plan = models.CharField(max_length=63)
