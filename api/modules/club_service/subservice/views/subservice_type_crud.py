from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework import status
from services.drf_classes.custom_permission import CustomPermission
from services.helpers.res_utils import ResUtils
from ..models import SubserviceType
from ..helpers.srs import SubserviceTypeSr


class SubserviceTypeViewSet(GenericViewSet):

    _name = "subservicetype"
    permission_classes = (CustomPermission,)
    serializer_class = SubserviceTypeSr
    search_fields = ["title"]

    def list(self, request):
        queryset = SubserviceType.objects.all()
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = SubserviceTypeSr(queryset, many=True)

        result = {
            "items": serializer.data,
        }

        return self.get_paginated_response(result)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(SubserviceType, pk=pk)
        serializer = SubserviceTypeSr(obj)
        return ResUtils.res(serializer.data)

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def add(self, request):
        serializer = SubserviceTypeSr(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return ResUtils.res(serializer.data)

    @transaction.atomic
    @action(methods=["put"], detail=True)
    def change(self, request, pk=None):
        obj = get_object_or_404(SubserviceType, pk=pk)
        data = request.data
        srs = SubserviceTypeSr(obj, data=data, partial=True)
        srs.is_valid(raise_exception=True)
        srs.save()
        return ResUtils.res(srs.data)

    @action(methods=["delete"], detail=True)
    def delete(self, request, pk=None):
        item = get_object_or_404(SubserviceType, pk=pk)
        item.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["delete"], detail=False)
    def delete_list(self, request):
        pk = self.request.query_params.get("ids", "")
        pks = [int(pk)] if pk.isdigit() else map(lambda x: int(x), pk.split(","))
        for pk in pks:
            item = get_object_or_404(SubserviceType, pk=pk)
            item.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)
