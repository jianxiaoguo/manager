import logging

import django
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response

from api import models, serializers
from api.exceptions import ServiceUnavailable
from api.viewset import NormalUserViewSet, DryccViewSet
from api.workflow_proxy import WorkflowProxy

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


# drycc manager request
class MeasurementsViewSet(DryccViewSet):

    def create(self, request, *args, **kwargs):
        for _ in request.data:
            _["cluster_id"] = request.cluster.pk
        return super(MeasurementsViewSet, self).create(request, **kwargs)


class MeasurementsConfigViewSet(MeasurementsViewSet):
    serializer_class = serializers.ConfigListSerializer


class MeasurementsVolumeViewSet(MeasurementsViewSet):
    serializer_class = serializers.VolumeListSerializer


class MeasurementsNetworksViewSet(MeasurementsViewSet):
    serializer_class = serializers.NetworkListSerializer


class MeasurementsInstancesViewSet(MeasurementsViewSet):
    serializer_class = serializers.InstanceListSerializer


class MeasurementsResourcesViewSet(MeasurementsViewSet):
    serializer_class = serializers.ResourceListSerializer


# UI request
class UserCsrfViewSet(NormalUserViewSet):
    def get(self, request, *args, **kwargs):
        import re
        token = re.findall(r'csrftoken=(.*?);', request.headers['Cookie']+';')[0]
        return Response({'token': token})
        # TODO debug
        # token = [_ for _ in request.headers['Cookie'].split('; ') if 'csrftoken' in _][0].split('=')[-1]
        # token = request.headers['Cookie'].split('csrftoken=')[-1]
        # res = Response({'token': token})
        # res.set_cookie('csrftoken', token, samesite=None, secure=True)
        # return res



class UserManagementViewSet(NormalUserViewSet):
    serializer_class = serializers.UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, many=False)
        return Response(serializer.data)


class ClustersViewSet(NormalUserViewSet):
    model = models.Cluster
    serializer_class = serializers.ClustersSerializer

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.all(*args, **kwargs)

    def get_object(self, **kwargs):
        cluster = get_object_or_404(self.model, cluster_id=kwargs['cluster_id'])
        return cluster


class ListViewSet(NormalUserViewSet):

    def get_queryset(self, **kwargs):
        serializer = self.serializer_class(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        serializerlist = serializers.ListSerializer(
            data=self.request.query_params)
        serializerlist.is_valid(raise_exception=True)
        q = Q(owner=self.request.user)
        if serializerlist.validated_data.get('section'):
            q &= Q(created__range=serializerlist.validated_data.get('section'))
        return self.model.objects.filter(q, **serializer.validated_data)


class BillsViewSet(ListViewSet):
    model = models.Bill
    serializer_class = serializers.BillsSerializer


class BillsProductViewSet(NormalUserViewSet):
    model = models.Bill
    serializer_class = serializers.BillsProductSerializer

    def get_queryset(self, **kwargs):
        serializer = serializers.BillsProductSerializer(
            data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        serializerlist = serializers.ListSerializer(
            data=self.request.query_params)
        serializerlist.is_valid(raise_exception=True)
        q = Q(owner=self.request.user)
        if serializerlist.validated_data.get('section'):
            q &= Q(created__range=serializerlist.validated_data.get('section'))
        return self.model.objects.filter(q, **serializer.validated_data).\
            order_by('resource_type', 'created').\
            extra(select={'created':"TO_CHAR(api_bill.created, 'YYYY-MM')"}).\
            values('resource_type', 'created').\
            annotate(sum_total_price=Sum('total_price'))


class BillsAppViewSet(NormalUserViewSet):
    model = models.Bill
    serializer_class = serializers.BillsProductSerializer

    def get_queryset(self, **kwargs):
        serializer = serializers.BillsProductSerializer(
            data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        serializerlist = serializers.ListSerializer(
            data=self.request.query_params)
        serializerlist.is_valid(raise_exception=True)
        q = Q(owner=self.request.user)
        if serializerlist.validated_data.get('section'):
            q &= Q(created__range=serializerlist.validated_data.get('section'))
        return self.model.objects.filter(q, **serializer.validated_data).\
            order_by('cluster__name', 'app_id', 'created').\
            extra(select={'created':"TO_CHAR(api_bill.created, 'YYYY-MM')"}).\
            values('created','cluster__name', 'app_id').\
            annotate(sum_total_price=Sum('total_price'))


class FundingsViewSet(ListViewSet):
    model = models.Funding
    serializer_class = serializers.FundingsSerializer


class MessagesViewSet(ListViewSet):
    model = models.Message
    serializer_class = serializers.MessagesSerializer


class MessageViewSet(NormalUserViewSet):
    model = models.Message
    serializer_class = serializers.MessagesSerializer

    def get_object(self):
        return get_object_or_404(self.model, uuid=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        msg = self.get_object()
        msg = serializers.MessagesSerializer(data=request.data,
                                             instance=msg,
                                             partial=True)
        msg.is_valid(raise_exception=True)
        msg.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClusterProxyViewSet(NormalUserViewSet):

    def get_cluster(self):
        cluster = get_object_or_404(models.Cluster,
                                    name=self.kwargs['name'])
        return cluster

    def list(self, request, *args, **kwargs):
        try:
            token = request.user.social_auth.filter(provider='drycc').last(). \
                extra_data.get('id_token')
        except AttributeError:
            return Response(status=401)
        cluster = self.get_cluster()
        wfp = WorkflowProxy(token).get(
            url=cluster.ingress + '/v2/' + kwargs.get('proxy_url'),
            **request.query_params)
        if wfp.status_code == 200:
            res = wfp.json()
            if not isinstance(res, dict):
                return Response(res)
            if res.get('previous'):
                res['previous'] = request.build_absolute_uri().split('?')[0] + \
                                  '?' + res['previous'].split('?')[1]
            if res.get('next'):
                res['next'] = request.build_absolute_uri().split('?')[0] + '?' \
                              + res['next'].split('?')[1]
            return Response(res)
        elif wfp.status_code in [401, 403, 404]:
            return Response(status=wfp.status_code)
        else:
            return Response(wfp.content, status=wfp.status_code)

    def delete(self, request, *args, **kwargs):
        try:
            token = request.user.social_auth.filter(provider='drycc').last(). \
                extra_data.get('id_token')
        except AttributeError:
            return Response(status=401)
        cluster = self.get_cluster()
        wfp = WorkflowProxy(token).delete(
            url=cluster.ingress + '/v2/' + kwargs.get('proxy_url'),
            **request.data)
        if wfp.status_code == 204:
            return Response(status=wfp.status_code)
        else:
            return Response(data=wfp.content, status=wfp.status_code)

    def post(self, request, *args, **kwargs):
        try:
            token = request.user.social_auth.filter(provider='drycc').last(). \
                extra_data.get('id_token')
        except AttributeError:
            return Response(status=401)
        cluster = self.get_cluster()
        wfp = WorkflowProxy(token).post(
            url=cluster.ingress + '/v2/' + kwargs.get('proxy_url'),
            **request.data)
        if wfp.status_code in [200]:
            return Response(wfp.json(), status=wfp.status_code)
        elif wfp.status_code in [201, 204]:
            return Response(status=wfp.status_code)
        else:
            return Response(data=wfp.content, status=wfp.status_code)
