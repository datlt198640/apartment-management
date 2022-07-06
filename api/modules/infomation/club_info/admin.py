from django.contrib import admin
from .models import ClubInfo


@admin.register(ClubInfo)
class ClubInfoAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
