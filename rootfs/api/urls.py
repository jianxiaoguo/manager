from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'accounts/', include('django.contrib.auth.urls')),

    # url(r'oauth/',
    #     include('oauth2_provider.urls', namespace='oauth2_provider')),
    url('', include('social_django.urls', namespace='social')),

    url(r'users/?$', views.UserDetailView.as_view({'get': 'retrieve'})),
    url(r'users/emails/?$', views.UserEmailView.as_view({'get': 'retrieve'})),

    url(r'^clusters/?$',
        views.ClustersViewSet.as_view({'get': 'list'})),
    url(r'^clusters/(?P<cluster_id>[-_\w]+)?$',
        views.ClustersViewSet.as_view({'get': 'retrieve'})),

    url(r'^clusters/(?P<cluster_id>[-_\w]+)/(?P<proxy_url>.+)/?$',
        views.ClusterProxyViewSet.as_view({'get': 'list',
                                           'post': 'post'})),

    url(r'^bills/?$',
        views.BillsViewSet.as_view({'get': 'list'})),
    url(r'^bills_by_product/?$',
        views.BillsProductViewSet.as_view({'get': 'list'})),

    url(r'^fundings/?$',
        views.FundingsViewSet.as_view({'get': 'list'})),
    url(r'^messages/?$',
        views.MessagesViewSet.as_view({'get': 'list'})),
    url(r'^message/(?P<pk>[-_\w]+)?$',
        views.MessageViewSet.as_view({'put': 'update'})),

    url(r'^measurements/config/?$',
        views.MeasurementsConfigViewSet.as_view({'post': 'create'})),
    url(r'^measurements/volumes/?$',
        views.MeasurementsVolumeViewSet.as_view({'post': 'create'})),
    url(r'^measurements/networks/?$',
        views.MeasurementsNetworksViewSet.as_view({'post': 'create'})),
    url(r'^measurements/instances/?$',
        views.MeasurementsInstancesViewSet.as_view({'post': 'create'})),
    url(r'^measurements/resources/?$',
        views.MeasurementsResourcesViewSet.as_view({'post': 'create'})),
]
