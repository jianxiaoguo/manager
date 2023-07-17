import logging
import hashlib
import calendar
import datetime
import stripe
import json
from django.utils import timezone
from django.conf import settings
from django.db.models import Q, Sum
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.middleware.csrf import get_token
from django.contrib.auth import get_user_model, logout as auth_logout
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.utils import (
    euro_cent_to_platform_credit, next_month, last_month, timestamp2datetime,
    date2timestamp)
from api import models, serializers
from api.exceptions import ServiceUnavailable, NotAuthenticated
from api.viewset import NormalUserViewSet, DryccViewSet
from api.drycc import DryccClient

User = get_user_model()
logger = logging.getLogger(__name__)


class ReadinessCheckView(View):
    """
    Simple readiness check view to determine DB connection / query.
    """

    def get(self, request):
        try:
            import django.db
            with django.db.connection.cursor() as c:
                c.execute("SELECT 0")
        except django.db.Error as e:
            raise ServiceUnavailable("Database health check failed") from e

        return HttpResponse("OK")

    head = get


class LivenessCheckView(View):
    """
    Simple liveness check view to determine if the server
    is responding to HTTP requests.
    """

    def get(self, request):
        return HttpResponse("OK")

    head = get


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        request.user.auth_token.delete()
    except Exception as e:
        logger.debug(e)
    auth_logout(request)
    return Response(status=status.HTTP_200_OK)


# drycc manager request
class MeasurementViewSet(DryccViewSet):

    serializer_class = serializers.MeasurementListSerializer

    def create(self, request, *args, **kwargs):
        for _ in request.data:
            _["cluster"] = request.cluster.pk
        return super(MeasurementViewSet, self).create(request, **kwargs)


class UserStatusViewSet(DryccViewSet):

    def status(self, request, *args, **kwargs):
        user = User.objects.filter(pk=kwargs["id"]).first()
        if not user or not user.is_active or user.status == 0:
            return Response({
                'is_active': False,
                'message': 'The user does not exist or is not activated.'
            })
        return Response({
            'is_active': True,
            'message': 'The user status is normal.'
        })


# UI request
class UserCsrfViewSet(NormalUserViewSet):

    def get(self, request, *args, **kwargs):
        return Response({
            'token': request.COOKIES.get("csrftoken", get_token(self.request))
        })


class UserAvatarViewSet(NormalUserViewSet):

    @method_decorator(cache_page(60 * 5))
    def avatar(self, request, *args, **kwargs):
        user = User.objects.filter(username=kwargs["username"]).first()
        size = request.GET.get("s", "80")
        md5 = hashlib.md5()
        if user:
            md5.update(user.email.encode("utf8"))
        return HttpResponseRedirect(settings.AVATAR_URL + md5.hexdigest() + "?s=" + size)


class UserManagementViewSet(NormalUserViewSet):
    serializer_class = serializers.UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, many=False)
        return Response(serializer.data)


class ChargeRuleViewSet(NormalUserViewSet, viewsets.ReadOnlyModelViewSet):
    model = models.charge.ChargeRule
    serializer_class = serializers.ChargeRuleSerializer

    def get_queryset(self):
        q = Q()
        name = self.request.GET.get("name")
        if name:
            q &= Q(name=name)
        cluster_id = self.request.GET.get("cluster_id")
        if cluster_id:
            q &= Q(cluster_id=cluster_id)
        cluster_type_list = self.request.GET.get("types", "").split(",")
        if len(cluster_type_list) > 0:
            q &= Q(type__in=cluster_type_list)
        return self.model.objects.filter(q)

    def calc(self, request, *args, **kwargs):
        total = 0
        items = []
        for item in request.data:
            rule = self.model.get(item["type"], item["unit"], item["usage"], item["cluster_id"])
            if rule:
                item = {
                    "type": item["type"],
                    "unit": item["unit"],
                    "price": rule.calc(item["usage"])
                }
                items.append(item)
                total += item["price"]
        return Response(data={"items": items, "total": total})


class ClusterViewSet(NormalUserViewSet, viewsets.ReadOnlyModelViewSet):
    model = models.cluster.Cluster
    serializer_class = serializers.ClusterSerializer

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.all(*args, **kwargs)

    def get_object(self, **kwargs):
        cluster = get_object_or_404(self.model, cluster_id=kwargs['cluster_id'])
        return cluster


class DryccProxyViewSet(NormalUserViewSet):

    @property
    def base_url(self):
        cluster = get_object_or_404(models.cluster.Cluster,
                                    uuid=self.kwargs['uuid'])
        return cluster.url + '/v2/'

    @property
    def client(self):
        try:
            social_auth = self.request.user.social_auth.filter(provider='drycc').last()
            extra_data = json.loads(social_auth.extra_data) if \
                isinstance(social_auth.extra_data, str) else social_auth.extra_data
            token = extra_data["id_token"]
        except AttributeError:
            raise NotAuthenticated()
        return DryccClient(token)

    def get(self, request, *args, **kwargs):
        response = self.client.get(
            self.base_url + kwargs.get('proxy_url'),
            **request.query_params
        )
        if response.status_code == 200 and "json" in response.headers.get('Content-Type'):
            data = response.json()
            if data.get('previous'):
                data['previous'] = request.build_absolute_uri().split('?')[0] + \
                                  '?' + data['previous'].split('?')[1]
            if data.get('next'):
                data['next'] = request.build_absolute_uri().split('?')[0] + '?' \
                              + data['next'].split('?')[1]
            return Response(data)
        return Response(
            data=response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type')
        )

    def delete(self, request, *args, **kwargs):
        response = self.client.delete(
            self.base_url + kwargs.get('proxy_url'),
            **request.data
        )
        return Response(
            data=response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type')
        )

    def post(self, request, *args, **kwargs):
        response = self.client.post(
            self.base_url + kwargs.get('proxy_url'),
            **request.data
        )
        return Response(
            data=response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type')
        )


class FundFlowViewSet(NormalUserViewSet, viewsets.ReadOnlyModelViewSet):
    model = models.fund.FundFlow
    serializer_class = serializers.FundFlowSerializer

    def get_queryset(self,  *args, **kwargs):
        period = self.request.GET.get("period", None)
        direction = self.request.GET.get("direction", None)
        trading_type = self.request.GET.get("trading_type", None)
        q = Q(owner=self.request.user)
        if not period:
            date = timezone.now().date()
            start = date2timestamp(datetime.date(year=date.year, month=date.month, day=1))
        else:
            start = int(period)
        start_time = timestamp2datetime(start)
        end = start + 3600 * 22 * calendar.monthrange(start_time.year, start_time.month)[1]
        q &= Q(period__gte=start, period__lte=end)
        if direction:
            q &= Q(direction=int(direction))
        if trading_type:
            q &= Q(trading_type=int(trading_type))
        return self.model.objects.filter(q)


class PrepaidCardViewSet(NormalUserViewSet, viewsets.ReadOnlyModelViewSet):
    model = models.fund.PrepaidCard
    serializer_class = serializers.PrepaidCardSerializer

    def get_object(self):
        return get_object_or_404(self.model, owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), many=False)
        return Response(serializer.data)


class BillViewSet(NormalUserViewSet, viewsets.ReadOnlyModelViewSet):
    model = models.bill.Bill
    serializer_class = serializers.BillSerializer

    def get_queryset(self):
        return self.model.objects.all()
        period = self.request.GET.get("period", None)
        app_id = self.request.GET.get("app_id", None)
        cluster_id = self.request.GET.get("cluster_id", None)
        q = Q(owner=self.request.user)
        if not period:
            _datetime = timezone.now().replace(day=self.request.user.invoice_day)
            if _datetime.day < self.request.user.invoice_day:
                start = int(date2timestamp(last_month(_datetime).date()))
            else:
                start = int(date2timestamp(_datetime.date()))
        else:
            start = int(period)
        end = int(date2timestamp(next_month(timestamp2datetime(start)).date()))
        q &= Q(period__gte=start, period__lte=end)
        if app_id:
            q &= Q(app_id=app_id)
        if cluster_id:
            q &= Q(cluster_id=cluster_id)
        return self.model.objects.filter(q)


class BillSummaryViewSet(BillViewSet):
    model = models.bill.Bill
    serializer_class = serializers.BillSummarySerializer

    def get_queryset(self):
        values = self.request.GET.get('values', 'app_id,type').split(',')
        return super().get_queryset().\
            order_by(*values).\
            values(*values).\
            annotate(price=Sum('price'))


class PaymentCardViewSet(NormalUserViewSet, viewsets.ReadOnlyModelViewSet):
    model = models.bill.PaymentCard
    serializer_class = serializers.PaymentCardSerializer

    def get_object(self):
        return get_object_or_404(self.model, owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_object(), many=False)
            return Response(serializer.data)
        except Http404:
            return Response({})


class InvoiceViewSet(NormalUserViewSet, viewsets.ReadOnlyModelViewSet):
    model = models.bill.Invoice
    serializer_class = serializers.InvoiceSerializer

    def get_object(self):
        return get_object_or_404(self.model, uuid=self.kwargs['pk'])

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user).order_by('-period')

    def get_serializer_class(self, *args, **kwargs):
        if 'pk' in self.kwargs:
            return serializers.InvoiceDetailSerializer
        return super().get_serializer_class(*args, **kwargs)


class InvoiceAddressViewSet(NormalUserViewSet, viewsets.ReadOnlyModelViewSet):
    model = models.bill.InvoiceAddress
    serializer_class = serializers.InvoiceAddressSerializer

    def get_object(self):
        return get_object_or_404(self.model, owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_object(), many=False)
            return Response(serializer.data)
        except Http404:
            return Response({})

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MessageViewSet(NormalUserViewSet):
    model = models.message.Message
    serializer_class = serializers.MessagesSerializer

    def get_object(self):
        return get_object_or_404(self.model, uuid=self.kwargs['pk'])

    def get_queryset(self):
        q = Q(receiver=self.request.user)
        unread = self.request.GET.get("unread")
        if unread == "true":
            q &= Q(unread=True)
        elif unread == "false":
            q &= Q(unread=False)
        return self.model.objects.filter(q)

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().receiver:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        msg = self.get_object()
        msg = serializers.MessagesSerializer(data=request.data,
                                             instance=msg,
                                             partial=True)
        msg.is_valid(raise_exception=True)
        msg.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def unread(self, request, *args, **kwargs):
        return Response(data={
            "unread": self.get_queryset().filter(unread=True).exists()
        })


class StripePaymentViewSet(viewsets.GenericViewSet):

    permission_classes = (AllowAny, )

    def public_key(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Response(data={"public_key": settings.STRIPE_PUBLIC_KEY})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def setup_intent(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            payment_card = models.bill.PaymentCard.objects.filter(owner=self.request.user).first()
            if payment_card and "customer_id" in payment_card.extra_data:
                customer_id = payment_card.extra_data["customer_id"]
            else:
                customer_id = stripe.Customer.create()['id']
            setup_intent = stripe.SetupIntent.create(
                customer=customer_id,
                payment_method_types=["card"],
            )
            return Response(setup_intent)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def _payment_method_attached(self, event):
        card = event.data["object"]["card"]
        other = event.data["object"]["metadata"]["other"]
        customer = event.data["object"]["customer"]
        payment_method = event.data["object"]["id"]
        billing_details = event.data["object"]["billing_details"]
        user = get_object_or_404(User, email=event.data["object"]["billing_details"]["email"])
        models.bill.PaymentCard.objects.update_or_create(
            owner=user,
            defaults={
                "name": billing_details["name"],
                "owner": user,
                "brand": card["brand"],
                "last4": card["last4"],
                "line1": billing_details["address"]["line1"],
                "line2": billing_details["address"]["line2"],
                "city": billing_details["address"]["city"],
                "state": billing_details["address"]["state"],
                "other": other,
                "country": billing_details["address"]["country"],
                "postcode": billing_details["address"]["postal_code"],
                "exp_year": card["exp_year"],
                "exp_month": card["exp_month"],
                "extra_data": {
                    "customer": customer,
                    "payment_method": payment_method,
                },
                "payment_provider": 1
            },
        )
        models.tax.ConsumerTaxInfo.objects.get_or_create(
            owner=user,
            defaults={
                "type": 2,
                "name": billing_details["name"],
                "city": billing_details["address"]["city"],
                "state": billing_details["address"]["state"],
                "country": billing_details["address"]["country"],
                "status": 0
            }
        )

    def _payment_intent_succeeded(self, event):
        amount = euro_cent_to_platform_credit(event.data["object"]["amount"])
        invoice_id = event.data["object"]["metadata"]["invoice_id"]
        invoice = get_object_or_404(models.bill.Invoice, uuid=invoice_id)
        assert invoice.unpaid == amount
        invoice.unpaid = 0
        invoice.paid += amount
        invoice.status = 2
        fund_flow = models.fund.FundFlow(
            owner=invoice.owner, direction=1, fund_type=1, trading_type=6,
            trading_channel=1, period=invoice.period, trading_id=invoice.uuid,
            remark='bank card payment'
        )
        fund_flow.amount = amount
        fund_flow.balance = 0
        fund_flow.save()
        invoice.save()

    def webhook_received(self, request, *args, **kwargs):
        payload = request.body.decode('utf-8')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=request.META['HTTP_STRIPE_SIGNATURE'],
            secret=settings.STRIPE_WEBHOOK_SECRET
        )
        if event.type == 'payment_intent.succeeded':
            self._payment_intent_succeeded(event)
        elif event.type == 'payment_method.attached':
            self._payment_method_attached(event)
        return Response(data={'status': 'success'})


class SettingsViewSet(viewsets.GenericViewSet):

    permission_classes = (AllowAny, )

    def retrieve(self, request, *args, **kwargs):
        return Response(data={
            "legal": settings.LEGAL_ENABLED,
            "billing_details": settings.BILLING_DETAILS,
        })


class ConsumerTaxInfoViewSet(NormalUserViewSet):
    model = models.tax.ConsumerTaxInfo
    serializer_class = serializers.ConsumerTaxInfoSerializer

    def types(self, request, *args, **kwargs):
        return Response(self.model.TYPE_CHOICES)

    def get_object(self):
        return get_object_or_404(self.model, owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_object(), many=False)
            return Response(serializer.data)
        except Http404:
            return Response({})

    def update(self, request, *args, **kwargs):
        user_tax_info = self.get_object()
        if user_tax_info.status == 1:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
