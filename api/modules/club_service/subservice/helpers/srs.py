from rest_framework.serializers import ModelSerializer
from ..models import Subservice, SubserviceCategory, SubserviceType
from datetime import datetime, timedelta, date


class SubserviceSr(ModelSerializer):
    class Meta:
        model = Subservice
        exclude = ()

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        open_time = datetime.strptime(rep["open_time"], '%H:%M:%S').time()
        delta = timedelta(minutes=int(rep["duration"]))
        fake_date = datetime.combine(date(1,1,1),open_time)
        rep["close_time"] =  (fake_date + delta).time()
        return rep
        
class SubserviceCategorySr(ModelSerializer):
    class Meta:
        model = SubserviceCategory
        exclude = ()

class SubserviceTypeSr(ModelSerializer):
    class Meta:
        model = SubserviceType
        exclude = ()
