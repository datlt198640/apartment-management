import os
import uuid
import qrcode
import datetime
from io import BytesIO
from django.utils import timezone
from django.core.files import File
from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.conf import settings
from services.models.timestamped_model import TimeStampedModel
from services.models.consts import GENDER_CHOICES
from .consts import BOOKING_STATUS_CHOICES, DEVICE_TYPE_CHOICES
from modules.club_service.service.models import Service
from rest_framework.serializers import ValidationError
# Create your models here.


def upload_to(instance, filename):
    ext = filename.split(".")[-1]
    return os.path.join("qr_code", f"{uuid.uuid4()}.{ext}")


def upload_avatar(instance, filename):
    ext = filename.split(".")[-1]
    return os.path.join("avatar", f"{uuid.uuid4()}.{ext}")


class Member(TimeStampedModel):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=128, null=True, default=None)
    dob = models.DateField(null=True)
    occupation = models.CharField(max_length=225, blank=True, default="")
    address = models.CharField(max_length=225, blank=True, default="")
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True, default=None)
    qr_code = models.ImageField(upload_to=upload_to, blank=True)
    avatar = models.ImageField(upload_to=upload_avatar, blank=True)
    services = models.ManyToManyField(
        Service, related_name="members", through="BookingService")

    def __str__(self):
        if self.full_name:
            return self.full_name
        else:
            return ""

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super().delete(*args, **kwargs)


    class Meta:
        db_table = "members"
        ordering = ["-user"]


class BookingService(TimeStampedModel):
    service = models.ForeignKey(
        Service, related_name="booking_service", on_delete=models.CASCADE)
    member = models.ForeignKey(
        Member, related_name="booking_service", blank=True, null=True, default=None, on_delete=models.CASCADE)
    # status = models.IntegerField(choices=BOOKING_STATUS_CHOICES)
    check_in = models.DateField(null=True, default=None)
    check_out = models.DateField(null=True, default=None)
    date = models.DateField(null=True, default=None)
    time = models.TimeField(null=True, default=None)
    adult = models.IntegerField(default=0, null=True)
    childs = models.IntegerField(default=0, null=True)
    participants = models.IntegerField(default=0, null=True)
    party_size = models.IntegerField(default=0, null=True)
    member_name = models.CharField(max_length=225, blank=True, default="")
    phone_number = models.CharField(max_length=225, blank=True, default="")
    email = models.CharField(max_length=225, blank=True, default="")
    deleted_at = models.DateTimeField(null=True, default=None, blank=True)

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        db_table = "booking_services"
        ordering = ["-id"]


class MemberShipType(TimeStampedModel):
    title = models.CharField(max_length=225, unique=True)
    services = models.ManyToManyField(Service, related_name="membership_type")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "membership_types"
        ordering = ["-id"]


class MemberShip(TimeStampedModel):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    membership_type = models.ForeignKey(
        MemberShipType, related_name="membership", on_delete=models.CASCADE, null=True)
    register_date = models.DateField(default=datetime.datetime.today)
    expire_date = models.DateField(default=datetime.datetime.today)

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super().delete(*args, **kwargs)

    class Meta:
        db_table = "memberships"
        ordering = ["-id"]


class Device(TimeStampedModel):
    type = models.IntegerField(
        choices=DEVICE_TYPE_CHOICES, null=True, blank=True)
    member = models.ForeignKey(
        Member, related_name="devices", on_delete=models.CASCADE)
    registration_token = models.CharField(max_length=225)

    class Meta:
        db_table = "devices"
        ordering = ["-id"]


@receiver(post_save, sender=Member)
def member_post_save(sender, instance, created, *args, **kwargs):
    if created:
        qrcode_img = qrcode.make(instance.uid)
        canvas = Image.new('RGB', (370, 370), 'white')
        canvas.paste(qrcode_img)
        fname = f'qr_code-{instance.uid}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        instance.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        instance.save()