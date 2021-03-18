from decimal import Decimal

from django.contrib import admin

from api.models import Cluster, Funding
from api.models.charge_rules import ChargeRule

is_superuser = True
empty_value_display = '-'
admin.site.site_header = 'Workflow Manager'
admin.site.site_title = 'Workflow Manager'


class ClusterAdmin(admin.ModelAdmin):
    list_display = ('name', 'ingress',)
    search_fields = ('name',)


class ChargeRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'resource_type', 'price_unit', 'price', 'created')
    search_fields = ('name', 'resource_type')


class FundingAdmin(admin.ModelAdmin):
    list_display = (
        'owner', 'operator', 'trade_type', 'credit', 'trade_credit', 'remark',
        'created')
    fieldsets = (
        ('base', {
            'fields': (
                'owner', 'trade_type', 'trade_credit', 'remark')
        }),
    )
    readonly_fields = ('owner', 'trade_type', 'credit', 'trade_credit',)

    def save_model(self, request, funding, form, change):
        try:
            credit = Funding.objects.filter(
                owner_id=request.POST['owner']).latest('created').credit
        except Funding.DoesNotExist:
            credit = 0
        trade_credit = request.POST.get('trade_credit')
        funding.credit = credit + Decimal(trade_credit)
        funding.operator = request.user.username
        funding.save()

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Cluster, ClusterAdmin)
admin.site.register(ChargeRule, ChargeRuleAdmin)
admin.site.register(Funding, FundingAdmin)
