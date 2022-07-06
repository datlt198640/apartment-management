from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.validators import UniqueValidator
from ..models import Promotion


class PromotionSr(ModelSerializer):
    class Meta:
        model = Promotion
        exclude = ()
