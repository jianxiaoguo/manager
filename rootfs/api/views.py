import logging

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from rest_framework import viewsets

from api import permissions, models, serializers
from api.exceptions import AlreadyExists, ServiceUnavailable

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


class ClustersViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAdmin]
    model = models.Clusters
    serializer_class = serializers.ClustersSerializer

    def get_cluster(self, *args, **kwargs):
        cluster = get_object_or_404(self.model, name=self.kwargs['name'])
        return cluster

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.all(*args, **kwargs)

    def get_object(self, **kwargs):
        cluster = self.get_cluster()
        return cluster

    def create(self, request, **kwargs):
        cluster = get_object_or_404(self.model, name=request.data['name'])
        if cluster:
            raise AlreadyExists("cluster {} already exist".format(cluster.name))
        return super(ClustersViewSet, self).create(request, **kwargs)
