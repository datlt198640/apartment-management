from django.db import models
from services.models.timestamped_model import TimeStampedModel
from services.models.consts import STATUS_SERVICE_CHOICES, SERVICE_TYPE_CHOICES


class SubserviceType(TimeStampedModel):
    title = models.CharField(max_length=225, unique=True)
    uid = models.CharField(max_length=225, unique=True, null=True, default=None)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "subservice_types"
        ordering = ["-id"]


class SubserviceCategory(TimeStampedModel):
    subservice_type = models.ForeignKey(SubserviceType, related_name="subservice_category", on_delete=models.CASCADE)
    title = models.CharField(max_length=225, unique=True)
    description = models.CharField(max_length=225, blank=True, default="")
    content = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "subservice_categories"
        ordering = ["-id"]



class Subservice(models.Model):
    subservice_category = models.ForeignKey(SubserviceCategory, related_name="subservice", on_delete=models.CASCADE)
    title = models.CharField(max_length=225, unique=True)
    description = models.CharField(max_length=225, blank=True, default="")
    content = models.TextField()
    price = models.FloatField(default=0.0)
    open_time = models.TimeField(null=True)
    duration = models.IntegerField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "subservices"
        ordering = ["-id"]
