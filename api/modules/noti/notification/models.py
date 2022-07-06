from django.db import models
from services.models.timestamped_model import TimeStampedModel
from modules.account.member.models import Member


class Notification(TimeStampedModel):
    member = models.ForeignKey(Member, related_name="notifications", on_delete=models.CASCADE, null=True, default=None)
    title=models.TextField()
    body=models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table="notifications"
        ordering=["-id"]
