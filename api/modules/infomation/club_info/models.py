from django.db import models

class ClubInfo(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255, blank=True, default="")
    content = models.TextField(blank=True, default="")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "club_infos"
        ordering = ["-id"]
