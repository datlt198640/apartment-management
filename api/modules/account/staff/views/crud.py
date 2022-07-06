from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework import status

from services.drf_classes.custom_permission import CustomPermission
from services.helpers.res_utils import ResUtils
from ..models import Staff
from ..helpers.srs import StaffSr, StaffRetrieveSr
from ..helpers.filters import StaffFilter
from ..helpers.model_utils import StaffModelUtils


class StaffViewSet(GenericViewSet):

    _name = "staff"
    permission_classes = (CustomPermission,)
    serializer_class = StaffSr
    filterset_class = StaffFilter
    search_fields = ["fullname"]

    def __init__(self, *args, **kwargs):
        self.mu = StaffModelUtils()

    def get_queryset(self):
        return Staff.objects.order_by("fullname")

    def list(self, request):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = StaffRetrieveSr(queryset, many=True)

        result = {
            "items": serializer.data,
            "extra": {
                "list_group": self.mu.get_list_group(),
            },
        }

        return self.get_paginated_response(result)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(Staff, pk=pk)
        serializer = StaffRetrieveSr(obj)
        return ResUtils.res(serializer.data)

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def add(self, request):
        data = request.data
        obj = self.mu.create_item(data)
        return ResUtils.res(StaffSr(obj).data)

    @transaction.atomic
    @action(methods=["put"], detail=True)
    def change(self, request, pk=None):
        obj = get_object_or_404(Staff, pk=pk)
        data = request.data
        obj = self.mu.update_item(obj, data)
        return ResUtils.res(StaffSr(obj).data)

    @action(methods=["delete"], detail=True)
    def delete(self, request, pk=None):
        item = get_object_or_404(Staff, pk=pk)
        item.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["delete"], detail=False)
    def delete_list(self, request):
        pk = self.request.query_params.get("ids", "")
        pks = [int(pk)] if pk.isdigit() else map(lambda x: int(x), pk.split(","))
        for pk in pks:
            item = get_object_or_404(Staff, pk=pk)
            item.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)
