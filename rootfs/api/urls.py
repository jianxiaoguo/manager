"""
URL routing patterns for the Drycc REST API.
"""
from django.conf.urls import include, url
from rest_framework.authtoken.views import \
    obtain_auth_token as views_obtain_auth_token
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/login/?$',
        views_obtain_auth_token),
    url(r'^clusters/?$',
        views.ClustersViewSet.as_view({'get': 'list',
                                       'post': 'create'})),
    url(r'^clusters/(?P<cluster_id>[-_\w]+)/?$',
        views.ClustersViewSet.as_view({'put': 'update',
                                       'delete': 'destroy'})),
    url(r'^clusters/(?P<cluster_id>[-_\w]+)/(?P<proxy_url>.+)/?$',
        views.ClusterProxyViewSet.as_view({'get': 'list'})),

    url(r'^measurements/config/?$',
        views.MeasurementConfigsViewSet.as_view({'post': 'create'})),
]
