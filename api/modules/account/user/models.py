from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone_number = PhoneNumberField(unique=True, verbose_name=("phone_number"))
    email = models.EmailField(unique=True, max_length=128, null=True, blank=True)

    token_context = models.CharField(max_length=256, blank=True, default="")
    token_signature = models.CharField(max_length=128, blank=True, default="")
    token_refresh_limit = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        db_table = "users"
        ordering = ["-id"]
        verbose_name = ("user")

    def clean(self):
        username_arr = [str(self.phone_number)]

        if not self.email:
            self.email = None
        else:
            username_arr.append(self.email)

        if not self.phone_number and not self.email:
            raise ValidationError(
                [("Email and phone number can not be blank together")],
                code="phone_number",
            )

        self.username = "-".join(username_arr)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
