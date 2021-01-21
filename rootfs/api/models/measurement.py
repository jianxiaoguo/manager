import logging
from django.db import models
from jsonfield import JSONField
from api.models import UuidAuditedModel
from api.models.clusters import Cluster

logger = logging.getLogger(__name__)


class MeasurementConfig(UuidAuditedModel):
    cluster = models.ForeignKey(Cluster, on_delete=models.PROTECT)
    app_id = models.CharField(max_length=63, db_index=True)
    owner_id = models.CharField(max_length=63, db_index=True)
    container_type = models.CharField(max_length=63)
    cpu = models.IntegerField()
    memory = models.IntegerField()
    timestamp = models.FloatField(db_index=True)


class MeasurementVolumes(UuidAuditedModel):
    cluster = models.ForeignKey(Cluster, on_delete=models.PROTECT)
    app_id = models.CharField(max_length=63, db_index=True)
    owner_id = models.CharField(max_length=63, db_index=True)
    name = models.CharField(max_length=63)
    size = models.IntegerField()
    timestamp = models.FloatField(db_index=True)
