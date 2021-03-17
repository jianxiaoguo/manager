"""
Classes to serialize the RESTful representation of Drycc API models.
"""
import logging
import json

from django.contrib.auth.models import User
from rest_framework import serializers
from api import models

logger = logging.getLogger(__name__)


class JSONFieldSerializer(serializers.JSONField):
    def __init__(self, *args, **kwargs):
        self.convert_to_str = kwargs.pop('convert_to_str', True)
        super(JSONFieldSerializer, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        """Deserialize the field's JSON data, for write operations."""
        try:
            val = json.loads(data)
        except TypeError:
            val = data
        return val

    def to_representation(self, obj):
        """Serialize the field's JSON data, for read operations."""
        for k, v in obj.items():
            if v is None:  # NoneType is used to unset a value
                continue

            try:
                if self.convert_to_str:
                    obj[k] = str(v)
            except ValueError:
                obj[k] = v
                # Do nothing, the validator will catch this later

        return obj


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name")


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class ClustersSerializer(serializers.ModelSerializer):
    """Serialize a :class:`~api.models.Cluster` model."""

    name = serializers.CharField(max_length=64)
    ingress = serializers.URLField(max_length=200)
    admin = serializers.CharField(max_length=64)
    passwd = serializers.CharField(max_length=128)

    class Meta:
        """Metadata options for a :class:`AppSerializer`."""
        model = models.Cluster
        fields = ['uuid', 'name', 'ingress', 'admin', 'passwd',
                  'created', 'updated']


class MeasurementConfigSerializer(serializers.ModelSerializer):
    """Serialize a :class:`~api.models.MeasurementConfig` model."""
    cluster_id = serializers.UUIDField()
    app_id = serializers.CharField(max_length=63)
    owner_id = serializers.CharField(max_length=63)
    container_type = serializers.CharField(max_length=63)
    cpu = serializers.IntegerField()
    memory = serializers.IntegerField()
    timestamp = serializers.FloatField()

    class Meta:
        """Metadata options for a :class:`MeasurementConfigSerializer`."""
        model = models.MeasurementConfig
        fields = ['cluster_id', 'app_id', 'owner_id', 'container_type', 'cpu',
                  'memory', 'timestamp']


class MeasurementConfigListSerializer(serializers.ListSerializer):
    """Serialize a :class:`~api.models.MeasurementConfig` model."""
    child = MeasurementConfigSerializer()
