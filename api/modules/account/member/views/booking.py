from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework import status, serializers
from rest_framework.exceptions import NotFound
from services.drf_classes.custom_permission import CustomPermission
from services.helpers.res_utils import ResUtils
from ..models import BookingService, Member
from ..helpers.srs import BookingServiceSr
from ..helpers.filters import BookingServiceFilter
from ..helpers.model_utils import MemberModelUtils
from modules.account.user.helpers.model_utils import UserModelUtils


class BookingServiceViewSet(GenericViewSet):

    _name = "bookingservice"
    permission_classes = (CustomPermission,)
    serializer_class = BookingServiceSr
    filterset_class = BookingServiceFilter
    search_fields = ["service__title", "member__full_name", "member_name", "phone_number", "email",
                     "adult", "childs", "participants", "party_size"]

    def __init__(self):
        self.user_mu = UserModelUtils()
        self.member_mu = MemberModelUtils()

    def list(self, request):
        queryset = BookingService.objects.filter(deleted_at=None)
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = BookingServiceSr(queryset, many=True)

        result = {
            "extra": {
                "list_service": self.member_mu.get_list_service(),
                "list_member": self.member_mu.get_list_member(),
                "list_membership_type": self.member_mu.get_list_membership_type()
            },
            "items": serializer.data,
        }

        return self.get_paginated_response(result)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(BookingService, pk=pk)
        if obj.deleted_at is not None:
            raise NotFound()
        serializer = BookingServiceSr(obj)
        return ResUtils.res(serializer.data)

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def add(self, request):
        data = request.data.copy()
        is_member = self.user_mu.is_member(request.user)
        if is_member:
            member = Member.objects.get(user=request.user)
            data["member"] = member.id
        else:
            raise serializers.ValidationError("Permission denied")
        serializer = BookingServiceSr(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return ResUtils.res(serializer.data)

    @transaction.atomic
    @action(methods=["put"], detail=True)
    def change(self, request, pk=None):
        obj = get_object_or_404(BookingService, pk=pk)
        data = request.data.copy()
        is_member = self.user_mu.is_member(request.user)
        if is_member:
            member = Member.objects.get(user=request.user)
            data["member"] = member.id
        else:
            raise serializers.ValidationError("Permission denied")
        srs = BookingServiceSr(obj, data=data, partial=True)
        srs.is_valid(raise_exception=True)
        srs.save()
        return ResUtils.res(srs.data)

    @action(methods=["delete"], detail=True)
    def delete(self, request, pk=None):
        item = get_object_or_404(BookingService, pk=pk)
        item.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["delete"], detail=False)
    def delete_list(self, request):
        pk = self.request.query_params.get("ids", "")
        pks = [int(pk)] if pk.isdigit() else map(
            lambda x: int(x), pk.split(","))
        for pk in pks:
            item = get_object_or_404(BookingService, pk=pk)
            item.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)
