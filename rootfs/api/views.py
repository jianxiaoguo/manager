import logging

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from rest_framework.response import Response
from api import models, serializers
from api.exceptions import AlreadyExists, ServiceUnavailable
from api.viewset import AdminViewSet, NormalUserViewSet, DryccViewSet
from proxy.workflow import WorkflowProxy

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


# admin request
class ClustersViewSet(AdminViewSet):
    # permission_classes = [permissions.IsAdmin]
    model = models.Cluster
    serializer_class = serializers.ClustersSerializer

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.all(*args, **kwargs)

    def get_object(self, **kwargs):
        cluster = get_object_or_404(self.model, cluster_id=kwargs['cluster_id'])
        return cluster

    def create(self, request, **kwargs):
        try:
            cluster = self.model.objects.get(name=self.request.data["name"])
        except self.model.DoesNotExist:
            cluster = None
        if cluster:
            raise AlreadyExists("cluster {} already exist".format(cluster.name))
        return super(ClustersViewSet, self).create(request, **kwargs)


# drycc controller request
class MeasurementConfigsViewSet(DryccViewSet):
    serializer_class = serializers.MeasurementConfigListSerializer

    def create(self, request, *args, **kwargs):
        for _ in request.data:
            _["cluster_id"] = request.cluster.pk
        return super(MeasurementConfigsViewSet, self).create(request, **kwargs)


# UI request
class ClusterProxyViewSet(NormalUserViewSet):

    def get_cluster(self):
        cluster = get_object_or_404(models.Cluster, pk=self.kwargs['cluster_id'])
        return cluster

    def list(self, request, *args, **kwargs):
        # todo debug
        request.user = User.objects.get(username='lijianguo')

        cluster = self.get_cluster()
        wfp = WorkflowProxy(cluster, request.user.username) \
            .get(url=cluster.ingress + '/v2/' + kwargs.get('proxy_url'), **kwargs)
        if wfp.status_code == 200:
            return Response(wfp.json())
        else:
            return Response(status=wfp.status_code)
