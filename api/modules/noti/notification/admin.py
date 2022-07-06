from django.contrib import admin
from .models import Notification
from services.helpers.fcm_message import FcmMessage
from modules.account.member.models import Device, Member, MemberShip


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "body")

    actions = ("send_public_notification",)

    def send_public_notification(self, request, queryset):
        for notification in queryset:
            if notification.member:
                member_devices = Device.objects.filter(member=notification.member)
                for member_device in member_devices:
                    device = member_device
                    title = notification.title
                    body = notification.body
                    FcmMessage().send_to_single_device(device, title, body)