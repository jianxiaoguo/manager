"""
Classes to serialize the RESTful representation of Drycc API models.
"""
import logging
import json

from django.contrib.auth.models import User
from django.utils import timezone
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

    @staticmethod
    def update_or_create(data):
        now = timezone.now()
        user, created = User.objects.update_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'first_name': data.get('first_name', ''),
                'last_name': data.get('first_name', ''),
                'last_login': now})
        if created:
            user.date_joined = now
            user.is_active = True
        if data.get('password'):
            user.set_password(data['password'])
        elif created and not data.get('password'):
            user.set_unusable_password()
        # Make the first signup an admin / superuser
        if not User.objects.filter(is_superuser=True).exists():
            user.is_superuser = user.is_staff = True
        user.save()
        return user

class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class ClustersSerializer(serializers.ModelSerializer):
    """Serialize a :class:`~api.models.Cluster` model."""

    name = serializers.CharField(max_length=64)
    ingress = serializers.URLField(max_length=200)

    class Meta:
        """Metadata options for a :class:`AppSerializer`."""
        model = models.Cluster
        fields = ['name', 'ingress', 'created', 'updated']


class BillsSerializer(serializers.ModelSerializer):
    """Serialize admin status for a Bill model."""
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = models.Bill
        fields = '__all__'
        read_only_fields = ['owner', 'cluster', 'app_id', 'resource_type',
                            'price_unit', 'price', 'quantity', 'total_price',
                            'start_time', 'end_time']


class BillsProductSerializer(serializers.Serializer):
    cluster_id = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.username')
    app_id = serializers.ReadOnlyField()
    resource_type = serializers.ReadOnlyField()
    sum_total_price = serializers.ReadOnlyField()


class FundingsSerializer(serializers.ModelSerializer):
    """Serialize admin status for a Funding model."""
    owner = serializers.ReadOnlyField(source='owner.username')
    trade_type = serializers.IntegerField(required=False)

    class Meta:
        model = models.Funding
        fields = '__all__'
        read_only_fields = ['operator', 'credit', 'trade_credit', 'owner']


class MessagesSerializer(serializers.ModelSerializer):
    """Serialize admin status for a Message model."""
    owner = serializers.ReadOnlyField(source='owner.username')
    code = serializers.ReadOnlyField()
    sender = serializers.ReadOnlyField()
    body = serializers.ReadOnlyField()
    is_deal = serializers.BooleanField(required=False)

    class Meta:
        model = models.Message
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.is_deal = validated_data.get('is_deal')
        instance.save()
        return instance


class ListSerializer(serializers.Serializer):
    section = serializers.CharField(max_length=500, required=False)

    @staticmethod
    def validate_section(section):
        field = section.split(',') if section else None
        import datetime
        if field is None:
            return None
        # else:
        #     try:
        #         start, stop = int(field[0]), int(field[1]) if field[
        #             1] else None  # noqa
        #     except ValueError as e:
        #         raise serializers.ValidationError(e)
        return [datetime.datetime.strptime(field[0], '%Y-%m-%d %H:%M:%S'),
                datetime.datetime.strptime(field[1], '%Y-%m-%d %H:%M:%S')]


class ConfigSerializer(serializers.ModelSerializer):
    """Serialize a :class:`~api.models.Config` model."""
    cluster_id = serializers.UUIDField()
    app_id = serializers.CharField(max_length=63)
    owner_id = serializers.CharField(max_length=63)
    container_type = serializers.CharField(max_length=63)
    cpu = serializers.IntegerField()
    memory = serializers.IntegerField()
    timestamp = serializers.FloatField()

    class Meta:
        """Metadata options for a :class:`ConfigSerializer`."""
        model = models.Config
        fields = ['cluster_id', 'app_id', 'owner_id', 'container_type', 'cpu',
                  'memory', 'timestamp']


class ConfigListSerializer(serializers.ListSerializer):
    """Serialize a :class:`~api.models.Config` model."""
    child = ConfigSerializer()


class VolumeSerializer(serializers.ModelSerializer):
    """Serialize a :class:`~api.models.Config` model."""
    cluster_id = serializers.UUIDField()
    app_id = serializers.CharField(max_length=63)
    owner_id = serializers.CharField(max_length=63)
    name = serializers.CharField(max_length=63)
    size = serializers.IntegerField()
    timestamp = serializers.FloatField()

    class Meta:
        """Metadata options for a :class:`VolumeSerializer`."""
        model = models.Config
        fields = ['cluster_id', 'app_id', 'owner_id', 'name', 'size',
                  'timestamp']


class VolumeListSerializer(serializers.ListSerializer):
    """Serialize a :class:`~api.models.Volume` model."""
    child = VolumeSerializer()


class NetworkSerializer(serializers.ModelSerializer):
    """Serialize a :class:`~api.models.Config` model."""
    cluster_id = serializers.UUIDField()
    app_id = serializers.CharField(max_length=63)
    owner_id = serializers.CharField(max_length=63)
    pod_name = serializers.CharField(max_length=63)
    rx_bytes = serializers.IntegerField()
    tx_bytes = serializers.IntegerField()
    timestamp = serializers.FloatField()

    class Meta:
        """Metadata options for a :class:`NetworkSerializer`."""
        model = models.Config
        fields = ['cluster_id', 'app_id', 'owner_id', 'pod_name', 'rx_bytes',
                  'tx_bytes', 'timestamp']


class NetworkListSerializer(serializers.ListSerializer):
    """Serialize a :class:`~api.models.Network` model."""
    child = NetworkSerializer()


class InstanceSerializer(serializers.ModelSerializer):
    """Serialize a :class:`~api.models.Instance` model."""
    cluster_id = serializers.UUIDField()
    app_id = serializers.CharField(max_length=63)
    owner_id = serializers.CharField(max_length=63)
    container_type = serializers.CharField(max_length=63)
    container_count = serializers.IntegerField()
    timestamp = serializers.FloatField()

    class Meta:
        """Metadata options for a :class:`InstanceSerializer`."""
        model = models.Config
        fields = ['cluster_id', 'app_id', 'owner_id', 'container_type',
                  'container_count',
                  'timestamp']


class InstanceListSerializer(serializers.ListSerializer):
    """Serialize a :class:`~api.models.Instance` model."""
    child = InstanceSerializer()


class ResourceSerializer(serializers.ModelSerializer):
    """Serialize a :class:`~api.models.Resource` model."""
    cluster_id = serializers.UUIDField()
    app_id = serializers.CharField(max_length=63)
    owner_id = serializers.CharField(max_length=63)
    name = serializers.CharField(max_length=63)
    plan = serializers.CharField(max_length=63)
    timestamp = serializers.FloatField()

    class Meta:
        """Metadata options for a :class:`ResourceSerializer`."""
        model = models.Config
        fields = ['cluster_id', 'app_id', 'owner_id', 'name', 'plan',
                  'timestamp']


class ResourceListSerializer(serializers.ListSerializer):
    """Serialize a :class:`~api.models.Resource` model."""
    child = ResourceSerializer()
