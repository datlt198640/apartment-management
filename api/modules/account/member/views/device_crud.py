from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from services.drf_classes.custom_permission import CustomPermission
from services.helpers.res_utils import ResUtils
from ..models import Device
from ..helpers.srs import DeviceSr
from ..helpers.model_utils import MemberModelUtils


class DeviceViewSet(GenericViewSet):
    _name = "device"
    serializer_class = DeviceSr
    permission_classes = (CustomPermission,)
    search_fields = ("title")

    def list(self, request):
        queryset = Device.objects.all()
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = DeviceSr(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(Device, pk=pk)
        serializer = DeviceSr(obj)
        return ResUtils.res(serializer.data)

    @action(methods=["post"], detail=True)
    def add(self, request):
        member = self.request.user.member
        registration_token = request.data.get("registration_token", None)

        serializer = DeviceSr(data=request.data)
        serializer.is_valid(raise_exception=True)

        MemberModelUtils().empty_device_token(member, registration_token)

        serializer.save()

        return ResUtils.res(serializer.data)

    @action(methods=["put"], detail=True)
    def change(self, request, pk=None):
        obj = get_object_or_404(Device, pk=pk)
        serializer = DeviceSr(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return ResUtils.res(serializer.data)

    @action(methods=["delete"], detail=True)
    def delete(self, request, registration_token=None):
        obj = get_object_or_404(Device, registration_token=registration_token)
        member = self.request.user.member
        Device.objects.filter(
            member=member, registration_token=registration_token
        ).delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)
