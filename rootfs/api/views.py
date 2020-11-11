"""
RESTful view classes for presenting Drycc API objects.
"""
from copy import deepcopy

from django.http import Http404, HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from guardian.shortcuts import assign_perm, get_objects_for_user, \
    get_users_with_perms, remove_perm
from django.views.generic import View
from django.db.models.deletion import ProtectedError
from rest_framework import mixins, renderers, status
from rest_framework.exceptions import PermissionDenied, NotFound, \
    AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authtoken.models import Token

import logging

logger = logging.getLogger(__name__)


class UserManagementViewSet(GenericViewSet):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        return self.get_queryset()[0]

    def list(self, request, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data)

    def destroy(self, request, **kwargs):
        if settings.LDAP_ENDPOINT:
            raise DryccException(
                "You cannot destroy user when ldap is enabled.")
        calling_obj = self.get_object()
        target_obj = calling_obj

        if request.data.get('username'):
            # if you "accidentally" target yourself, that should be fine
            if calling_obj.username == request.data[
                'username'] or calling_obj.is_superuser:
                target_obj = get_object_or_404(User, username=request.data[
                    'username'])
            else:
                raise PermissionDenied()

        # A user can not be removed without apps changing ownership first
        if len(models.App.objects.filter(owner=target_obj)) > 0:
            msg = '{} still has applications assigned. Delete or transfer ownership'.format(
                str(target_obj))  # noqa
            raise AlreadyExists(msg)

        try:
            target_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError as e:
            raise AlreadyExists(e)

    def passwd(self, request, **kwargs):
        if not request.data.get('new_password'):
            raise DryccException("new_password is a required field")
        if settings.LDAP_ENDPOINT:
            raise DryccException(
                "You cannot change password when ldap is enabled.")

        caller_obj = self.get_object()
        target_obj = self.get_object()
        if request.data.get('username'):
            # if you "accidentally" target yourself, that should be fine
            if caller_obj.username == request.data[
                'username'] or caller_obj.is_superuser:
                target_obj = get_object_or_404(User, username=request.data[
                    'username'])
            else:
                raise PermissionDenied()

        if not caller_obj.is_superuser:
            if not request.data.get('password'):
                raise DryccException("password is a required field")
            if not target_obj.check_password(request.data['password']):
                raise AuthenticationFailed('Current password does not match')

        target_obj.set_password(request.data['new_password'])
        target_obj.save()
        return Response({'status': 'password set'})


class TokenManagementViewSet(GenericViewSet,
                             mixins.DestroyModelMixin):
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.CanRegenerateToken]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        return self.get_queryset()[0]

    def regenerate(self, request, **kwargs):
        obj = self.get_object()

        if 'all' in request.data:
            for user in User.objects.all():
                if not user.is_anonymous:
                    token = Token.objects.get(user=user)
                    token.delete()
                    Token.objects.create(user=user)
            return Response("")

        if 'username' in request.data:
            obj = get_object_or_404(User,
                                    username=request.data['username'])
            self.check_object_permissions(self.request, obj)

        token = Token.objects.get(user=obj)
        token.delete()
        token = Token.objects.create(user=obj)
        return Response({'token': token.key})

    def token(self, request, **kwargs):
        if self.request.user.username == kwargs['username'] \
                or self.request.user.is_superuser:
            obj = get_object_or_404(User, username=kwargs['username'])
            token = Token.objects.get(user=obj)
            return Response({'token': token.key})
        return Response(status=status.HTTP_403_FORBIDDEN)


class AdminPermsViewSet(BaseDryccViewSet):
    """RESTful views for sharing admin permissions with other users."""

    model = User
    serializer_class = serializers.AdminUserSerializer
    permission_classes = [permissions.IsAdmin]

    def get_queryset(self, **kwargs):
        self.check_object_permissions(self.request, self.request.user)
        return self.model.objects.filter(is_active=True, is_superuser=True)

    def create(self, request, **kwargs):
        user = get_object_or_404(self.model, username=request.data['username'])
        user.is_superuser = user.is_staff = True
        user.save(update_fields=['is_superuser', 'is_staff'])
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, **kwargs):
        user = get_object_or_404(self.model, username=kwargs['username'])
        user.is_superuser = user.is_staff = False
        user.save(update_fields=['is_superuser', 'is_staff'])
        return Response(status=status.HTTP_204_NO_CONTENT)
