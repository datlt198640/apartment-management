from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from services.drf_classes.custom_permission import CustomPermission
from services.helpers.res_utils import ResUtils
from ..models import ClubInfo
from ..helpers.srs import ClubInfoSr


class ClubInfoViewSet(GenericViewSet):
    _name = "clubinfo"
    serializer_class = ClubInfoSr
    permission_classes = (CustomPermission,)
    search_fields = ("title",)

    def list(self, request):
        queryset = ClubInfo.objects.all()
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = ClubInfoSr(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(ClubInfo, pk=pk)
        serializer = ClubInfoSr(obj)
        return ResUtils.res(serializer.data)

    @action(methods=["post"], detail=True)
    def add(self, request):
        serializer = ClubInfoSr(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return ResUtils.res(serializer.data)

    @action(methods=["put"], detail=True)
    def change(self, request, pk=None):
        obj = get_object_or_404(ClubInfo, pk=pk)
        serializer = ClubInfoSr(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return ResUtils.res(serializer.data)

    @action(methods=["delete"], detail=True)
    def delete(self, request, pk=None):
        obj = get_object_or_404(ClubInfo, pk=pk)
        obj.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["delete"], detail=False)
    def delete_list(self, request):
        pk = self.request.query_params.get("ids", "")
        pk = [int(pk)] if pk.isdigit() else map(lambda x: int(x), pk.split(","))
        result = ClubInfo.objects.filter(pk__in=pk)
        if result.count() == 0:
            raise Http404
        result.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)
