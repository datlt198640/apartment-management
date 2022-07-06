from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework import status

from services.drf_classes.custom_permission import CustomPermission
from services.helpers.res_utils import ResUtils
from ..models import Service
from ..helpers.srs import ServiceSr
from ..helpers.model_utils import ServiceModelUtils


class ServiceViewSet(GenericViewSet):

    _name = "service"
    permission_classes = (CustomPermission,)
    serializer_class = ServiceSr
    search_fields = ["title"]

    def __init__(self, *args, **kwargs):
        self.mu = ServiceModelUtils()

    def list(self, request):
        queryset = Service.objects.all()
        queryset = self.filter_queryset(queryset)
        serializer = ServiceSr(queryset, many=True)

        result = {
            "items": serializer.data,
        }

        return ResUtils.res(result)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(Service, pk=pk)
        serializer = ServiceSr(obj)
        return ResUtils.res(serializer.data)

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def add(self, request):
        images = request.FILES.getlist('image_url')
        data = request.data.copy()
        data["image_url"] = images
        obj = self.mu.create_item(data)
        return ResUtils.res(ServiceSr(obj).data)

    @transaction.atomic
    @action(methods=["put"], detail=True)
    def change(self, request, pk=None):
        obj = get_object_or_404(Service, pk=pk)
        images = request.FILES.getlist('image_url')
        data = request.data.copy()
        data["image_url"] = images
        obj = self.mu.update_item(obj, data)
        return ResUtils.res(ServiceSr(obj).data)

    @action(methods=["delete"], detail=True)
    def delete(self, request, pk=None):
        item = get_object_or_404(Service, pk=pk)
        item.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["delete"], detail=False)
    def delete_list(self, request):
        pk = self.request.query_params.get("ids", "")
        pks = [int(pk)] if pk.isdigit() else map(lambda x: int(x), pk.split(","))
        for pk in pks:
            item = get_object_or_404(Service, pk=pk)
            item.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)
