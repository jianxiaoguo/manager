from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api import permissions, authentication


class AdminViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for objects filtered by their 'owner' attribute.

    To use it, at minimum you'll need to provide the `serializer_class` attribute and
    the `model` attribute shortcut.
    """
    permission_classes = [permissions.IsAdmin]


class NormalUserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for objects filtered by their 'owner' attribute.

    To use it, at minimum you'll need to provide the `serializer_class` attribute and
    the `model` attribute shortcut.
    """
    permission_classes = [IsAuthenticated]


class DryccViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for objects filtered by their 'owner' attribute.

    To use it, at minimum you'll need to provide the `serializer_class` attribute and
    the `model` attribute shortcut.
    """
    permission_classes = [permissions.IsDrycc]
    authentication_classes = (authentication.AnonymousAuthentication, )
