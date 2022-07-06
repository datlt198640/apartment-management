from django.contrib import admin
from .models import Subservice, SubserviceCategory, SubserviceType


@admin.register(Subservice)
class SubserviceAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "price", "subservice_category")

@admin.register(SubserviceCategory)
class SubserviceCategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)

@admin.register(SubserviceType)
class SubserviceTypeAdmin(admin.ModelAdmin):
    list_display = ("title",)
