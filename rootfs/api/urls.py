"""
URL routing patterns for the Drycc REST API.
"""
from django.conf.urls import include, url
from rest_framework.authtoken.views import obtain_auth_token as views_obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r'^', include(router.urls)),
    # authn / authz
    url(r'^auth/login/$',
        views_obtain_auth_token)
]
