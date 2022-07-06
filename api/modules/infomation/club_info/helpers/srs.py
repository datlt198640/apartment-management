from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.validators import UniqueValidator
from ..models import ClubInfo


class ClubInfoSr(ModelSerializer):
    class Meta:
        model = ClubInfo
        exclude = ()
