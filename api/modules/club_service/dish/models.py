from django.db import models
from services.models.timestamped_model import TimeStampedModel
from modules.club_service.service.models import Service


class DishCategory(models.Model):
    title = models.CharField(max_length=64, unique=True)
    service = models.ManyToManyField(Service, related_name="dish_categories", through = "Dish")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "dish_category"
        ordering = ["-id"]


class Dish(TimeStampedModel):
    dish_category = models.ForeignKey(DishCategory, related_name="dish", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name="dish", on_delete=models.CASCADE)
    title = models.CharField(max_length=225, unique=True)
    description = models.CharField(max_length=225, blank=True, default="")
    content = models.TextField()
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "dishes"
        ordering = ["-id"]