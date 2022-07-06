import os
import uuid
from django.db import models
from services.models.timestamped_model import TimeStampedModel
import datetime
from modules.account.member.models import Member
from .consts import NotiStatusChoices


def upload_to(instance, filename):
    ext = filename.split(".")[-1]
    return os.path.join("event", f"{uuid.uuid4()}.{ext}")


class Event(TimeStampedModel):
    member = models.ManyToManyField(Member, through="EventMember")
    title = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255, blank=True, default="")
    content = models.TextField(blank=True, default="")
    start_time = models.DateTimeField(default=datetime.datetime.now)
    end_time = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "events"
        ordering = ["-id"]


class EventMember(TimeStampedModel):
    event = models.ForeignKey(
        Event, related_name="event_member", on_delete=models.CASCADE)
    member = models.ForeignKey(
        Member, related_name="event_member", blank=True, null=True, on_delete=models.CASCADE)
    member_name = models.CharField(max_length=225, blank=True, default="")
    phone_number = models.CharField(max_length=225, blank=True, default="")
    email = models.CharField(max_length=225, blank=True, default="")

    class Meta:
        db_table = "event_members"
        ordering = ["-id"]


class ImageEvent(TimeStampedModel):
    event = models.ForeignKey(
        Event, related_name="image_event", on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)

    class Meta:
        db_table = "image_events"
        ordering = ["-id"]
