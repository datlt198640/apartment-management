from django_filters import rest_framework as filters
from ..models import BookingService
from services.models.consts import SERVICE_TYPE_CHOICES


class BookingServiceFilter(filters.FilterSet):

    type = filters.NumberFilter(field_name='service__type')


    class Meta:
        model = BookingService
        exclude = []
