"""
Classes to serialize the RESTful representation of Drycc API models.
"""
import logging

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from api import models
from api.utils import timestamp2datetime

User = get_user_model()
logger = logging.getLogger(__name__)


class ListSerializer(serializers.Serializer):
    section = serializers.CharField(max_length=500, required=False)

    @staticmethod
    def validate_section(section):
        field = section.split(',') if section else None
        if field is None:
            return None
        return [timestamp2datetime(float(field[0])),
                timestamp2datetime(float(field[1]))]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'is_superuser',
                  'is_staff', 'groups', 'user_permissions', 'last_login', 'date_joined',
                  'is_active']
        read_only_fields = ['id', 'is_superuser', 'is_staff', 'groups',
                            'user_permissions', 'last_login', 'date_joined', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    @staticmethod
    def update_or_create(data):
        now = timezone.now()
        user, created = User.objects.update_or_create(
            id=data['id'],
            defaults={
                "email": data['email'],
                "username": data['username'],
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "is_staff": data['is_staff'],
                "is_active": data['is_active'],
                "is_superuser": data['is_superuser'],
                'last_login': now
            }
        )
        if created:
            user.date_joined = now
            user.set_unusable_password()
        user.save()
        return user, created


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class ClusterSerializer(serializers.ModelSerializer):
    """Serialize a :class:`~api.models.Cluster` model."""

    name = serializers.CharField(max_length=64)
    url = serializers.URLField(max_length=200)

    class Meta:
        """Metadata options for a :class:`AppSerializer`."""
        model = models.cluster.Cluster
        fields = ['uuid', 'name', 'url', 'created', 'updated']


class BillSerializer(serializers.ModelSerializer):
    """Serialize admin status for a Bill model."""

    class Meta:
        model = models.bill.Bill
        fields = '__all__'


class BillSummarySerializer(serializers.Serializer):
    app_id = serializers.ReadOnlyField()
    type = serializers.ReadOnlyField()
    price = serializers.ReadOnlyField()

    class Meta:
        model = models.bill.Bill


class PaymentCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.bill.PaymentCard
        fields = ('name', 'brand', 'last4', 'line1', 'line2', 'city', 'state', 'country', 'other')


class InvoiceSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = models.bill.Invoice
        fields = ('uuid', 'owner', 'period', 'status')


class InvoiceDetailSerializer(InvoiceSerializer):
    bill_summary = serializers.JSONField(read_only=True, allow_null=True)
    payment_methods = serializers.JSONField(read_only=True, allow_null=True)

    class Meta:
        model = models.bill.Invoice
        fields = '__all__'


class InvoiceAddressSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.pk')

    class Meta:
        model = models.bill.InvoiceAddress
        fields = '__all__'


class ChargeRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.charge.ChargeRule
        fields = '__all__'


class PrepaidCardSerializer(serializers.ModelSerializer):
    """Serialize admin status for a Funding model."""

    class Meta:
        model = models.fund.PrepaidCard
        fields = '__all__'


class FundFlowSerializer(serializers.ModelSerializer):
    """Serialize admin status for a Funding model."""
    direction = serializers.CharField(source='get_direction_display')
    fund_type = serializers.CharField(source='get_fund_type_display')
    trading_type = serializers.CharField(source='get_trading_type_display')
    trading_channel = serializers.CharField(source='get_trading_channel_display')

    class Meta:
        model = models.fund.FundFlow
        fields = '__all__'


class MessagesSerializer(serializers.ModelSerializer):
    """Serialize admin status for a Message model."""
    type = serializers.ReadOnlyField(source='get_type_display')
    body = serializers.ReadOnlyField()
    unread = serializers.BooleanField(default=True)
    sender = serializers.ReadOnlyField(source='sender.username')
    receiver = serializers.ReadOnlyField(source='receiver.username')

    def update(self, instance, validated_data):
        instance.unread = validated_data.get('unread')
        instance.save()
        return instance

    class Meta:
        model = models.message.Message
        fields = '__all__'


class MeasurementSerializer(serializers.ModelSerializer):
    """Serialize a :class:`~api.models.Config` model."""
    app_id = serializers.CharField(max_length=64)
    owner = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, queryset=User.objects.all()
    )
    name = serializers.CharField(max_length=64)
    type = serializers.CharField(max_length=64)
    unit = serializers.CharField(max_length=16)
    usage = serializers.IntegerField()
    timestamp = serializers.IntegerField()
    cluster = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, queryset=models.cluster.Cluster.objects.all()
    )

    class Meta:
        """Metadata options for a :class:`ConfigSerializer`."""
        model = models.measurement.Measurement
        fields = '__all__'


class MeasurementListSerializer(serializers.ListSerializer):
    """Serialize a :class:`~api.models.MeasurementSerializer` model."""
    child = MeasurementSerializer()


class ConsumerTaxInfoSerializer(serializers.ModelSerializer):

    status = serializers.IntegerField(read_only=True)
    provider = serializers.JSONField(read_only=True)

    class Meta:
        """Metadata options for a :class:`ConfigSerializer`."""
        model = models.tax.ConsumerTaxInfo
        fields = '__all__'
