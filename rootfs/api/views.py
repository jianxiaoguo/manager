from django.shortcuts import get_object_or_404
from rest_framework import viewsets

import logging
from api import permissions, models, serializers
from api.exceptions import AlreadyExists

logger = logging.getLogger(__name__)


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
