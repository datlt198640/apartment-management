from django.contrib import admin
from .models import Service, ServiceTime, ImageService


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "type", "bookable", "has_menu")

@admin.register(ServiceTime)
class ServiceTimeAdmin(admin.ModelAdmin):
    list_display = ("service",)

@admin.register(ImageService)
class ImageServiceAdmin(admin.ModelAdmin):
    list_display = ("service",)
