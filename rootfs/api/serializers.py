"""
Classes to serialize the RESTful representation of Drycc API models.
"""
import logging
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


class ClustersSerializer(serializers.ModelSerializer):
    """Serialize a :class:`~api.models.Clusters` model."""

    name = serializers.CharField(max_length=64)
    domain = serializers.URLField(max_length=200)
    admin = serializers.CharField(max_length=64)
    passwd = serializers.CharField(max_length=128)

    class Meta:
        """Metadata options for a :class:`AppSerializer`."""
        model = models.Clusters
        fields = ['uuid', 'name', 'domain', 'admin', 'passwd', 'created', 'updated']

