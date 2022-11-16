from django.db import models
from django.core.cache import cache
from django.contrib.auth import get_user_model
from .base import UuidAuditedModel
User = get_user_model()


class ProviderTaxInfo(UuidAuditedModel):
    no = models.CharField(max_length=128, null=True, blank=True, db_index=True)
    rate = models.PositiveSmallIntegerField()
    city = models.CharField(max_length=64, null=True, blank=True)
    state = models.CharField(max_length=64, null=True, blank=True)
    country = models.CharField(max_length=64)

    @classmethod
    def get(cls, country, state, city):
        def _get():
            country_q = models.Q(country=country)
            state_q = models.Q(state=state) \
                | models.Q(state__isnull=True) | models.Q(city__exact='')
            city_q = models.Q(city=city) \
                | models.Q(city__isnull=True) | models.Q(city__exact='')
            provider = cls.objects.filter(country_q, state_q, city_q).order_by(
                models.F('state').desc(nulls_last=True)
            ).order_by(models.F('city').desc(nulls_last=True)).first()
            if provider is None:
                provider = cls.objects.get(no="default")
            return provider

        key = f"service_provider:{country}:{state}:{city}"
        return cache.get_or_set(key, _get, 3600)

    class Meta:
        unique_together = (("country", "state", "city"),)


class ConsumerTaxInfo(UuidAuditedModel):
    TYPE_CHOICES = (
        (1, 'company'),
        (2, 'individual/sole trader'),
        (3, 'non-profit'),
    )
    STATUS_CHOICES = [
        (0, 'not verified'),
        (1, 'verified'),
    ]
    no = models.CharField(max_length=128, null=True, blank=True)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    name = models.CharField(max_length=64)
    owner = models.OneToOneField(User, on_delete=models.PROTECT)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    status = models.PositiveSmallIntegerField(db_index=True, choices=STATUS_CHOICES)

    @property
    def provider(self):
        no, rate = "", 0
        if self.status == 1:
            tax_rate = ProviderTaxInfo.get(self.country, self.state, self.city)
            if tax_rate.no is not None and tax_rate.no != "default":
                no = tax_rate.no
            rate = tax_rate.rate
        return {"no": no, "rate": rate}
