from django.contrib import admin
from .models import CheckIn
from .forms import CheckInForm

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ("member", "check_in", "check_out")
    # form = CheckInForm