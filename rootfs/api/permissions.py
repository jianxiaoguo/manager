import base64
from django.core import serializers
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser

from api import models


class IsAnonymous(permissions.BasePermission):
    """
    View permission to allow anonymous users.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return request.method == 'GET' and type(request.user) is AnonymousUser


class IsAdmin(permissions.BasePermission):
    """
    View permission to allow only admins.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return request.user.is_superuser


class IsDrycc(permissions.BasePermission):
    """
    View permission to allow only admins.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.META.get("HTTP_AUTHORIZATION"):
            token = request.META.get(
                "HTTP_AUTHORIZATION").split(" ")[1].encode("utf8")
            access_key, secret_key = base64.b85decode(token).decode("utf8").split(":")
            data = cache.get(access_key)
            if data:
                request.cluster = next(serializers.deserialize("json", data)).object
            else:
                request.cluster = get_object_or_404(
                    models.cluster.Cluster, pk=access_key, secret=secret_key)
                data = serializers.serialize('json', [request.cluster], ensure_ascii=False)
                cache.set(access_key, data)
            return True
        return False
