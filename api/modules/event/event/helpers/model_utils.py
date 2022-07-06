from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from services.models.repo import Repo
from .srs import EventSr, EventMemberSr, ImageEventSr
from ..models import ImageEvent, Event, EventMember
from modules.account.member.models import Member, MemberShipType
from modules.account.member.helpers.srs import MemberSr, MemberShipTypeSr


def add_image(images, event_obj):
    if images:
        for image in images:
            image_obj = {'event': event_obj.pk, 'image_url': image}
            img_sr = ImageEventSr(data=image_obj)
            img_sr.is_valid(raise_exception=True)
            img_sr.save()


class EventModelUtils:
    def __init__(self, model=None):
        self.model = Repo.load(Repo.EVENT)

    def seeding(self, index: int, single: bool = False, save: bool = True) -> QuerySet:

        if index == 0:
            raise Exception("Indext must be start with 1.")

        def get_data(i: int) -> dict:

            data = {
                "title": f"title{i}",
                "description": f"description{i}",
                "content": f"content{i}",
                "start_date": f"2022-01-{i}",
                "end_date": f"2022-01-{i}",
            }
            if save is False:
                return data
            try:
                instance = self.model.objects.get(title=data["title"])
            except self.model.DoesNotExist:
                instance = EventSr(data=data)
                instance.is_valid(raise_exception=True)
                instance = instance.save()
            return instance

        def get_list_data(index):
            return [get_data(i) for i in range(1, index + 1)]

        return get_data(index) if single is True else get_list_data(index)

    def create_item(self, data):
        event_sr = EventSr(data=data)
        event_sr.is_valid(raise_exception=True)
        event = event_sr.save()

        images = data.get("image_url", [])
        add_image(images, event)
        return event

    def update_item(self, obj, data):
        for image in obj.image_event.all():
            item = get_object_or_404(ImageEvent, pk=image.pk)
            item.delete()
        images = data.get("image_url", [])
        add_image(images, obj)
        sr = EventSr(obj, data=data, partial=True)
        sr.is_valid(raise_exception=True)
        return sr.save()

    def get_list_member(self):
        queryset = Member.objects.all()
        members = MemberSr(queryset, many=True).data
        return [{"label": member["full_name"], "value": member["id"]} for member in members]

    def get_list_event(self):
        queryset = Event.objects.all()
        events = EventSr(queryset, many=True).data
        return [{"label": event["title"], "value": event["id"]} for event in events]

    def get_list_event_booking(self, event_member_queryset):
        event_booking_queryset = []

        for event_member in event_member_queryset:
            if event_member.event not in event_booking_queryset:
                event_booking_queryset.append(event_member.event)

        event_bookings = EventSr(event_booking_queryset, many=True).data
        return [{"label": event_booking["title"], "value": event_booking["id"]} for event_booking in event_bookings]

    def get_list_membership_type(self) -> list :
        membership_type = MemberShipType.objects.all()
        membership_type_srs = MemberShipTypeSr(membership_type, many=True)
        return [{"value": data["id"], "label": data["title"]} for data in membership_type_srs.data]