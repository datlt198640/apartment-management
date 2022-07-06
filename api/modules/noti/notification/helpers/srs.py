from rest_framework.serializers import ModelSerializer
from ..models import Notification

class NotificationSr(ModelSerializer):
    class Meta:
        model = Notification
        exclude = ()

