from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http.request import QueryDict
from rest_framework.serializers import ModelSerializer

from services.helpers.utils import Utils
from modules.account.user.helpers.model_utils import UserModelUtils
from ..models import Staff

Model = Staff


class StaffSr(ModelSerializer):
    class Meta:
        model = Model
        exclude = []

    def to_internal_value(self, obj):
        obj = obj.dict() if isinstance(obj, QueryDict) else obj

        json_list = ["vinmec_sites"]
        [Utils.ensure_json(obj, key) for key in json_list]
        return super().to_internal_value(obj)

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        groups = obj.user.groups.all()

        rep["fullname"] = obj.fullname
        rep["email"] = obj.user.email or ""
        rep["phone_number"] = str(obj.user.phone_number or "")
        rep["is_active"] = obj.user.is_active
        rep["is_active_label"] = "YES" if obj.user.is_active else ""
        rep["groups"] = groups.values_list("id", flat=True)
        rep["group_labels"] = groups.values_list("name", flat=True)
        return rep


class StaffRetrieveSr(StaffSr):
    class Meta(StaffSr.Meta):
        exclude = [
            "created_at",
            "updated_at",
            "user",
        ]


class StaffPermissionSr(StaffRetrieveSr):
    class Meta(StaffRetrieveSr.Meta):
        pass

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        rep["permissions"] = UserModelUtils.get_permissions(obj.user)
        return rep


class StaffOptionSr(StaffSr):
    class Meta(StaffSr.Meta):
        exclude = []

    def to_representation(self, obj):
        groups = obj.user.groups.all()
        return {
            "value": obj.id,
            "label": obj.fullname,
            "email": obj.user.email,
            "phone_number": str(obj.user.phone_number),
            "groups": groups.values_list("id", flat=True),
            "group_labels": groups.values_list("name", flat=True),
        }
