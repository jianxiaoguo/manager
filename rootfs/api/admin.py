import time
from django.contrib import admin
from api.models.cluster import Cluster
from api.models.bill import Bill, Invoice, InvoiceAddress, PaymentCard
from api.models.fund import FundFlow
from api.models.fund import PrepaidCard
from api.models.measurement import Measurement
from api.models.charge import ChargeRule
from api.models.message import Message
from api.models.tax import ProviderTaxInfo, ConsumerTaxInfo

is_superuser = True
empty_value_display = '-'
admin.site.site_header = 'Workflow Manager'
admin.site.site_title = 'Workflow Manager'


class ClusterAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'secret')
    search_fields = ('pk', 'name',)


class ChargeRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'unit', 'price', 'created')
    search_fields = ('name', 'type')


class PrepaidCardAdmin(admin.ModelAdmin):
    list_display = ('owner_id', 'status', 'amount')
    list_filter = ('status', )
    search_fields = ('owner_id', )

    def save_model(self, request, obj, form, change):
        if change:
            timestamp = time.time()
            period = int(timestamp - timestamp % 3600)
            prepaid_card = PrepaidCard.objects.get(pk=obj.pk)
            if prepaid_card.amount > obj.amount:  # account adjustment
                FundFlow(
                    owner=obj.owner,
                    direction=2,
                    fund_type=1,
                    trading_type=1,
                    trading_channel=1,
                    period=period,
                    amount=prepaid_card.amount-obj.amount,
                    balance=obj.amount,
                    remark=f'{request.user.username} change prepaid card',
                ).save()
            elif prepaid_card.amount < obj.amount:  # recharge
                FundFlow(
                    owner=obj.owner,
                    direction=1,
                    fund_type=1,
                    trading_type=2,
                    trading_channel=5,
                    period=period,
                    amount=obj.amount-prepaid_card.amount,
                    balance=obj.amount,
                    remark=f'{request.user.username} change prepaid card',
                ).save()
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False


class FundFlowAdmin(admin.ModelAdmin):
    list_display = ('owner_id', 'direction', 'fund_type', 'trading_type', 'amount')
    search_fields = ('owner_id', )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BillAdmin(admin.ModelAdmin):
    list_display = ('app_id', 'owner_id', 'price', 'period', 'cluster')
    list_filter = ('uuid', 'app_id', 'owner_id')
    search_fields = ('uuid', )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PaymentCardAdmin(admin.ModelAdmin):
    list_display = ('owner_id', 'brand', 'last4', 'country')
    search_fields = ('uuid', 'owner_id')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('owner_id', 'price', 'period', 'status')
    list_filter = ('uuid', 'owner_id')
    search_fields = ('uuid', )

    # def has_add_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


class InvoiceAddressAdmin(admin.ModelAdmin):
    list_display = ('owner_id', 'country', 'state', 'city')
    search_fields = ('owner_id', )


class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('app_id', 'owner_id', 'name', 'type', 'unit', 'usage')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'type', 'unread')
    search_fields = ('sender', 'receiver', 'created')


class ProviderTaxInfoAdmin(admin.ModelAdmin):
    list_display = ('no', 'rate', 'city', 'state', 'country')
    search_fields = ('no', 'country', 'state', 'city')


class ConsumerTaxInfoAdmin(admin.ModelAdmin):
    list_display = ('no', 'name', 'status', 'city', 'state', 'country')
    search_fields = ('no', 'name', 'status')


admin.site.register(Cluster, ClusterAdmin)
admin.site.register(ChargeRule, ChargeRuleAdmin)
admin.site.register(PrepaidCard, PrepaidCardAdmin)
admin.site.register(FundFlow, FundFlowAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(PaymentCard, PaymentCardAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceAddress, InvoiceAddressAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(ProviderTaxInfo, ProviderTaxInfoAdmin)
admin.site.register(ConsumerTaxInfo, ConsumerTaxInfoAdmin)
