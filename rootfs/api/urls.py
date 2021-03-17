from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import \
    obtain_auth_token as views_obtain_auth_token
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r'^', include(router.urls)),

    url('accounts/', include('django.contrib.auth.urls')),

    url('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    url('users/?$', views.UserDetailView.as_view({'get': 'retrieve'})),
    url('users/emails/?$', views.UserEmailView.as_view({'get': 'retrieve'})),

    # url(r'^clusters/?$',
    #     views.ClustersViewSet.as_view({'get': 'list',
    #                                    'post': 'create'})),
    # url(r'^clusters/(?P<cluster_id>[-_\w]+)/?$',
    #     views.ClustersViewSet.as_view({'put': 'update',
    #                                    'delete': 'destroy'})),

    url(r'^clusters/?$',
        views.ClustersViewSet.as_view({'get': 'list'})),
    url(r'^clusters/(?P<cluster_id>[-_\w]+)?$',
        views.ClustersViewSet.as_view({'get': 'retrieve'})),

    url(r'^clusters/(?P<cluster_id>[-_\w]+)/(?P<proxy_url>.+)/?$',
        views.ClusterProxyViewSet.as_view({'get': 'list',
                                           'post': 'post'})),

    url(r'^measurements/config/?$',
        views.MeasurementConfigsViewSet.as_view({'post': 'create'})),
]
