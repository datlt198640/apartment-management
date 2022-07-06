from django.db import models
from services.models.timestamped_model import TimeStampedModel
from modules.account.member.models import Member


class CheckIn(TimeStampedModel):
    member = models.ForeignKey(Member, related_name="check_in", on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True, default=None)
    is_check_out = models.BooleanField(default=False)
    

    def save(self, *args, **kwargs):
        self.clean()
        self.is_check_out = self.check_out is not None
        super().save(*args, **kwargs)

    class Meta:
        db_table = "check_ins"
        ordering = ["-id"]

