import os
import uuid
from django.db import models
from services.models.timestamped_model import TimeStampedModel
from services.models.consts import SERVICE_TYPE_CHOICES
from modules.club_service.subservice.models import SubserviceType


def upload_to(instance, filename):
    ext = filename.split(".")[-1]
    return os.path.join("sevice", f"{uuid.uuid4()}.{ext}")

class Service(TimeStampedModel):
    subservice_type = models.ForeignKey(SubserviceType, related_name="service", blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255, blank=True, default="")
    content = models.TextField(blank=True, default="")
    bookable = models.BooleanField(default=False)
    has_menu = models.BooleanField(default=False)
    type = models.IntegerField(choices=SERVICE_TYPE_CHOICES)


    def __str__(self):
        return self.title

    class Meta:
        db_table = "services"
        ordering = ["-id"]


class ServiceTime(TimeStampedModel):
    service = models.OneToOneField(Service, on_delete=models.CASCADE)
    open_time = models.TimeField(null=True)
    close_time = models.TimeField(null=True)

    class Meta:
        db_table = "service_times"
        ordering = ["-id"]

class ImageService(TimeStampedModel):
    service = models.ForeignKey(Service, related_name="image_service",on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)

    class Meta:
        db_table = "image_services"
        ordering = ["-id"]
