from django.db import models
from django.conf import settings

from services.models.timestamped_model import TimeStampedModel
from services.models.consts import GENDER_CHOICES

# Create your models here.


class Staff(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=128)
    gender = models.IntegerField(choices=GENDER_CHOICES)

    def __str__(self):
        return self.fullname

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super().delete(*args, **kwargs)

    class Meta:
        db_table = "staffs"
        ordering = ["-user"]
