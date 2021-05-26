from decimal import Decimal

from django import forms
from django.contrib import admin

from api.models import Cluster, Funding, Bill
from api.models.charge_rules import ChargeRule

is_superuser = True
empty_value_display = '-'
admin.site.site_header = 'Workflow Manager'
admin.site.site_title = 'Workflow Manager'


class ClusterAdmin(admin.ModelAdmin):
    list_display = ('name', 'ingress',)
    search_fields = ('name',)


class ChargeRuleForm(forms.ModelForm):
    def clean_price_unit(self):
        price_unit_data = self.cleaned_data['price_unit']
        resource_type_data = self.cleaned_data['resource_type']
        credit_unit, measurement_unit, time_unit = price_unit_data.split(r'/')
        print(price_unit_data)
        if time_unit not in ['hour', 'day'] or \
                (resource_type_data == 1 and measurement_unit not in [
                    'mcores']) or \
                (resource_type_data in [2, 3] and measurement_unit not in [
                    'MB']) or \
                (resource_type_data == 4 and measurement_unit not in (
                'bytes')):  # noqa
            raise forms.ValidationError('price_unit is invalid')
        return price_unit_data

    def clean_price(self):
        price = self.cleaned_data['price']
        if self.cleaned_data['price'] < 0:
            raise forms.ValidationError('price must be a positive number')
        return price

    class Meta:
        model = ChargeRule
        fields = ('name', 'resource_type', 'price_unit', 'price')
        help_texts = {
            'price_unit': 'example: credit/MB/day,credit/mcores/day,credit/bytes/hour', # noqa
        }


class ChargeRuleAdmin(admin.ModelAdmin):
    form = ChargeRuleForm
    list_display = ('name', 'resource_type', 'price_unit', 'price', 'created')
    search_fields = ('name', 'resource_type')


class FundingAdmin(admin.ModelAdmin):
    list_display = (
        'uuid', 'owner', 'operator', 'trade_type', 'credit', 'trade_credit',
        'bill', 'remark', 'created')
    fieldsets = (
        ('base', {
            'fields': (
                'owner', 'trade_type', 'trade_credit', 'remark')
        }),
    )
    list_filter = ('uuid', 'owner', 'trade_type')

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

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BillAdmin(admin.ModelAdmin):
    list_display = (
        'uuid', 'owner', 'cluster', 'app_id', 'charge_rule_info',
        'resource_info', 'total_price', 'start_time', 'end_time', 'created')
    list_filter = ('uuid', 'cluster', 'owner')
    search_fields = ('uuid', )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Cluster, ClusterAdmin)
admin.site.register(ChargeRule, ChargeRuleAdmin)
admin.site.register(Funding, FundingAdmin)
admin.site.register(Bill, BillAdmin)
