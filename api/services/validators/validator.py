# from rest_framework.serializers import ValidationError
from django.core.exceptions import ValidationError

from phonenumber_field.phonenumber import to_python
from utils.helpers.utils import Utils


def password_validator(value):
    errors = Utils.password_validate(value)
    if errors:
        raise ValidationError(errors, code="invalid")


def phone_number_validator(value):
    phone_number = to_python(value)
    if phone_number and not phone_number.is_valid():
        raise ValidationError(
            [("Invalid phone number format")], code="invalid_phone_number"
        )
