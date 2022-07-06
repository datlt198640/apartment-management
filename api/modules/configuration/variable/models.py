from django.db import models
from .consts import SettingVariables

class VariableManager(models.Manager):
    def get_value(self, uid: str, default_value: str = "") -> str:
        try:
            item = self.get(uid=uid)
            return item.value
        except Variable.DoesNotExist:
            if hasattr(SettingVariables, uid):
                return getattr(SettingVariables, uid)
            return default_value
# Create your models here.


class Variable(models.Model):
    uid = models.CharField(max_length=64, unique=True)
    value = models.CharField(max_length=255, blank=True, default="")

    objects = VariableManager()

    def __str__(self):
        return f"{self.uid} = {self.value}"

    class Meta:
        db_table = "variables"
        ordering = ["-id"]
