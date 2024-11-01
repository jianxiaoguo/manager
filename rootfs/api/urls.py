from django.urls import include, re_path
from api import views

urlpatterns = [
    re_path(r'logout/', views.logout),
    re_path(
        r"settings/?$",
        views.SettingsViewSet.as_view({'get': 'retrieve'})),
    re_path(
        r'^auth/csrf/?$',
        views.UserCsrfViewSet.as_view({'get': 'get'})),
    re_path(
        r'^auth/whoami/?$',
        views.UserManagementViewSet.as_view({'get': 'retrieve'})),
    re_path(
        r'^avatar/(?P<username>[-_\w]+)/?$',
        views.UserAvatarViewSet.as_view({'get': 'avatar'})),
    re_path(
        r'^clusters/?$',
        views.ClusterViewSet.as_view({'get': 'list'})),
    re_path(
        r'^clusters/(?P<name>[-_\w]+)?$',
        views.ClusterViewSet.as_view({'get': 'retrieve'})),
    re_path(
        r'^clusters/(?P<uuid>[-_\w]+)/(?P<proxy_url>.+)/?$',
        views.DryccProxyViewSet.as_view({
            'get': 'get', 'delete': 'delete', 'post': 'post', 'put': 'put'
        })),
    re_path(
        r'^bills/?$',
        views.BillViewSet.as_view({'get': 'list'})),
    re_path(
        r'^bills_summary/?$',
        views.BillSummaryViewSet.as_view({'get': 'list'})),
    re_path(
        r'^account/my_payment_card/?$',
        views.PaymentCardViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    re_path(
        r'^account/invoices/?$',
        views.InvoiceViewSet.as_view({'get': 'list'})),
    re_path(
        r'^account/invoices/(?P<pk>[-_\w]+)/?$',
        views.InvoiceViewSet.as_view({'get': 'retrieve'})),
    re_path(
        r'^account/my_invoice_address/?$',
        views.InvoiceAddressViewSet.as_view({
            'get': 'retrieve', 'post': 'create', 'put': 'update', 'delete': 'destroy'})),
    re_path(
        r'^funds/flows/?$',
        views.FundFlowViewSet.as_view({'get': 'list'})),
    re_path(
        r'^funds/balance/?$',
        views.PrepaidCardViewSet.as_view({'get': 'retrieve'})),
    re_path(
        r'^messages/?$',
        views.MessageViewSet.as_view({'get': 'list'})),
    re_path(
        r'^messages/unread/?$',
        views.MessageViewSet.as_view({'get': 'unread'})),
    re_path(
        r'^messages/(?P<pk>[-_\w]+)/?$',
        views.MessageViewSet.as_view({'put': 'update', 'delete': 'destroy'})),

    re_path(
        r'^measurements/?$',
        views.MeasurementViewSet.as_view({'post': 'create'})),
    re_path(
        r'^users/(?P<id>[-_\w]+)/status/?$',
        views.UserStatusViewSet.as_view({'get': 'status'})),

    re_path(
        r'^pricing/?$',
        views.ChargeRuleViewSet.as_view({'get': 'list'})),
    re_path(
        r'^pricing/calc/?$',
        views.ChargeRuleViewSet.as_view({'post': 'calc'})),
    # stripe webhook
    re_path(
        r'^payments/stripe/public-key/?$',
        views.StripePaymentViewSet.as_view({'get': 'public_key'})),
    re_path(
        r'^payments/stripe/setup-intent/?$',
        views.StripePaymentViewSet.as_view({'post': 'setup_intent'})),
    re_path(
        r'^payments/stripe/webhook-received/?$',
        views.StripePaymentViewSet.as_view({'post': 'webhook_received'})),
    # tax ServiceProviderViewSet ConsumerTaxInfoViewSet
    re_path(
        r'^taxs/consumer-tax-info/?$',
        views.ConsumerTaxInfoViewSet.as_view(
            {'get': 'retrieve', 'post': 'create', 'put': 'update'})),
    re_path(
        r'^taxs/consumer-tax-info/types/?$',
        views.ConsumerTaxInfoViewSet.as_view({'get': 'types'})),

    re_path(r'accounts/', include('django.contrib.auth.urls')),

    # social login is placed at the end of the URL match
    re_path('', include('social_django.urls', namespace='social')),
]
