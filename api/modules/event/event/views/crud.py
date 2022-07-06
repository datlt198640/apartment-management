from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from services.drf_classes.custom_permission import CustomPermission
from services.helpers.res_utils import ResUtils
from ..models import Event
from ..helpers.srs import EventSr
from ..helpers.model_utils import EventModelUtils


class EventViewSet(GenericViewSet):
    _name = "event"
    serializer_class = EventSr
    permission_classes = (CustomPermission,)
    search_fields = ("title", "start_date", "end_date")

    def __init__(self):
        self.mu = EventModelUtils()

    def list(self, request):
        queryset = Event.objects.all()
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = EventSr(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(Event, pk=pk)
        serializer = EventSr(obj)
        return ResUtils.res(serializer.data)

    @action(methods=["post"], detail=True)
    def add(self, request):
        images = request.FILES.getlist('image_url')
        data = request.data.copy()
        data["image_url"] = images
        obj = self.mu.create_item(data)
        return ResUtils.res(EventSr(obj).data)

    @action(methods=["put"], detail=True)
    def change(self, request, pk=None):
        obj = get_object_or_404(Event, pk=pk)
        images = request.FILES.getlist('image_url')
        data = request.data.copy()
        data["image_url"] = images
        obj = self.mu.update_item(obj, data)
        return ResUtils.res(EventSr(obj).data)

    @action(methods=["delete"], detail=True)
    def delete(self, request, pk=None):
        obj = get_object_or_404(Event, pk=pk)
        obj.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["delete"], detail=False)
    def delete_list(self, request):
        pk = self.request.query_params.get("ids", "")
        pk = [int(pk)] if pk.isdigit() else map(lambda x: int(x), pk.split(","))
        result = Event.objects.filter(pk__in=pk)
        if result.count() == 0:
            raise Http404
        result.delete()
        return ResUtils.res(status=status.HTTP_204_NO_CONTENT)