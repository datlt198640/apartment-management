from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework import status

from services.drf_classes.custom_permission import CustomPermission
from services.helpers.res_utils import ResUtils
from ..models import Member
from ..helpers.srs import MemberSr, MemberRetrieveSr, MemberPermissionSr
from ..helpers.model_utils import MemberModelUtils




class MemberViewSet(GenericViewSet):

    _name = "member"
    permission_classes = (CustomPermission,)
    serializer_class = MemberSr
    search_fields = ["full_name", "user__email",
                     "user__phone_number", "occupation", "address"]

    def __init__(self, *args, **kwargs):
        self.mu = MemberModelUtils()

    def get_queryset(self):
        return Member.objects.exclude(member_remote_id = None)

    def list(self, request):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        items = MemberPermissionSr(queryset, many=True).data
        if not settings.DEBUG:
            member_remotes = self.mu.get_list_member_from_remote_db()
            for item in items:
                for member_remote in member_remotes:
                    if item["member_remote_id"] == member_remote["member_remote_id"]:
                        self.mu.convert_key_member(item, member_remote)
        result = {
            "items": items,
            "extra": {
                "list_group": self.mu.get_list_group(),
                "list_membership_type": self.mu.get_list_membership_type(),
            },
        }

        return self.get_paginated_response(result)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(Member, pk=pk)
        result = MemberRetrieveSr(obj).data
        if settings.DEBUG:
            result = self.mu.get_member_from_remote_db(pk)
        return ResUtils.res(result)

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def add(self, request):
        data = request.data
        obj = self.mu.create_item(data)
        return ResUtils.res(MemberSr(obj).data)

    @transaction.atomic
    @action(methods=["put"], detail=True)
    def change(self, request, pk=None):
        obj = get_object_or_404(Member, pk=pk)
        data = request.data
        obj = self.mu.update_item(obj, data)
        if not settings.DEBUG:
            result = self.mu.update_member_from_remote_db(obj.member_remote_id, data)
        return ResUtils.res(result)

    @action(methods=["delete"], detail=True)
    def delete(self, request, pk=None):
        item = get_object_or_404(Member, pk=pk)
        item.delete()
        if not settings.DEBUG:
            self.mu.remove_member_from_remote_db(item.member_remote_id)
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["delete"], detail=False)
    def delete_list(self, request):
        pk = self.request.query_params.get("ids", "")
        pks = [int(pk)] if pk.isdigit() else map(
            lambda x: int(x), pk.split(","))
        for pk in pks:
            item = get_object_or_404(Member, pk=pk)
            item.delete()
            if not settings.DEBUG:
                self.mu.remove_member_from_remote_db(item.member_remote_id)
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)
