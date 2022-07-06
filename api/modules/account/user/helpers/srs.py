from django.http.request import QueryDict
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError
from services.helpers.utils import Utils
from services.models.repo import Repo

User = Repo.load_user()


class LoginSr(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=65)


class UserSr(ModelSerializer):
    class Meta:
        model = User
        exclude = []

    def to_internal_value(self, obj):
        obj = obj.dict() if isinstance(obj, QueryDict) else obj

        email = obj.get("email", None)
        if email:
            email = email.lower()
            obj["email"] = email

        phone_number = obj.get("phone_number", None)
        if phone_number:
            phone_number = phone_number.lower()
            phone_number = Utils.phone_to_canonical_format(phone_number) or None
            obj["phone_number"] = phone_number

        obj["username"] = f"{phone_number}_{email or ''}"

        if "password" in obj and obj["password"] != Utils.get_unusable_password():
            password = obj["password"]
            if error_msg := Utils.password_validate(password):
                raise ValidationError({"detail": error_msg})
            obj["password"] = make_password(password)

        [Utils.ensure_json(obj, key) for key in ["groups"]]

        return super().to_internal_value(obj)
