from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import Group
from modules.account.user.helpers.model_utils import UserModelUtils


class GroupSr(ModelSerializer):
    class Meta:
        model = Group
        fields = [
            "id",
            "name",
        ]

    def create(self, validated_data):
        permission_source = self.initial_data.get("permissions", "")
        permissions = [
            int(permission)
            for permission in permission_source.split(",")
            if permission.isdigit()
        ]

        group = Group(**validated_data)
        group.save()
        group.permissions.set(permissions)

        return group


class GroupOptionSr(ModelSerializer):
    class Meta:
        model = Group
        exclude = []

    def to_representation(self, obj):
        return dict(
            value=obj.id,
            label=obj.name,
            is_manager=UserModelUtils.is_manager_group(obj),
        )
