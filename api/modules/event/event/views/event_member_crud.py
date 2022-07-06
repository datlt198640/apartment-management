import datetime
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from services.drf_classes.custom_permission import CustomPermission
from services.helpers.res_utils import ResUtils
from ..models import EventMember, Event
from ..helpers.model_utils import EventModelUtils
from ..helpers.srs import EventMemberSr
from ..helpers.filters import EventMemberFilter


class EventMemberViewSet(GenericViewSet):
    _name = "eventmember"
    serializer_class = EventMemberSr
    permission_classes = (CustomPermission,)
    search_fields = ("event__title", "member__full_name", "member_name", "phone_number", "email") 
    filterset_class = EventMemberFilter

    def __init__(self):
        self.mu = EventModelUtils()

    def list(self, request):
        now = datetime.datetime.now()
        queryset = EventMember.objects.filter(event__end_time__gt=now)
        list_event_booking = self.mu.get_list_event_booking(queryset)
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = EventMemberSr(queryset, many=True)

        result = {
            "items": serializer.data,
            "extra": {
                "list_member": self.mu.get_list_member(),
                "list_event": self.mu.get_list_event(),
                "list_event_booking": list_event_booking,
                "list_membership_type": self.mu.get_list_membership_type()
            },
        }

        return self.get_paginated_response(result)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(EventMember, pk=pk)
        serializer = EventMemberSr(obj)
        return ResUtils.res(serializer.data)

    @action(methods=["post"], detail=True)
    def add(self, request):
        member = self.request.user.member
        data = request.data.copy()
        data["member"] = member.pk
        serializer = EventMemberSr(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return ResUtils.res(serializer.data)

    @action(methods=["put"], detail=True)
    def change(self, request, pk=None):
        member = self.request.user.member
        data = request.data.copy()
        data["member"] = member.pk
        obj = get_object_or_404(EventMember, pk=pk)
        serializer = EventMemberSr(obj, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return ResUtils.res(serializer.data)

    @action(methods=["delete"], detail=True)
    def delete(self, request, pk=None):
        obj = get_object_or_404(EventMember, pk=pk)
        obj.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["delete"], detail=False)
    def delete_list(self, request):
        pk = self.request.query_params.get("ids", "")
        pk = [int(pk)] if pk.isdigit() else map(
            lambda x: int(x), pk.split(","))
        result = EventMember.objects.filter(pk__in=pk)
        if result.count() == 0:
            raise Http404
        result.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)
