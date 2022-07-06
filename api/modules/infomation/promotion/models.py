from django.db import models
from services.models.timestamped_model import TimeStampedModel
import datetime

class Promotion(TimeStampedModel):
    title = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255, blank=True, default="")
    content = models.CharField(max_length=255, blank=True, default="")
    start_date = models.DateField(default=datetime.datetime.today)
    end_date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "promotions"
        ordering = ["-id"]
