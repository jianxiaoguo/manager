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
        return type(request.user) is AnonymousUser


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
            cluster_id = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
            request.cluster = get_object_or_404(models.Cluster, pk=cluster_id)
            return True
        else:
            return False
