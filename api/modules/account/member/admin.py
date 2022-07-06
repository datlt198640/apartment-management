from django.contrib import admin
from django.core.mail import send_mail
from .models import Member, MemberShip, MemberShipType, BookingService, Device

@admin.register(BookingService)
class BookingServiceAdmin(admin.ModelAdmin):
    list_display = ("service", "member", "deleted_at", "member_name", "phone_number", "email")
    search_fields = ["service__title", "member__full_name", "deleted_at","member_name", "phone_number", "email"]
    actions = ["send_email_booking_member"]

    def send_email_booking_member(self, request, queryset):

        for booking in queryset:
            print("booking", booking.member)

        send_mail(
            'Subject here',
            'Here is the message.',
            'ltdat1001@gmail.com',
            ['ltdat1001@gmail.com'],
            fail_silently=False,
        )

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("uid", "user", "full_name")

@admin.register(MemberShip)
class MemberShipAdmin(admin.ModelAdmin):
    list_display = ("id", "member")

@admin.register(MemberShipType)
class MemberShipTypeAdmin(admin.ModelAdmin):
    list_display = ("title",)
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("type", "registration_token")
