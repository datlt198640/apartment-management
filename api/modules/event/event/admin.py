from django.contrib import admin
from .models import Event, EventMember, ImageEvent


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "start_time", "end_time")


@admin.register(EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    list_display = ("event", "member")

@admin.register(ImageEvent)
class ImageEventAdmin(admin.ModelAdmin):
    list_display = ("event",)
