from django_filters import rest_framework as filters
from ..models import CheckIn


CHECK_OUT_CHOICES = (
    (0, 'Not check out'),
    (1, 'Checked out'),
)

class CheckInFilter(filters.FilterSet):

    start_check_in = filters.DateTimeFilter(field_name="check_in", lookup_expr="gte")
    end_check_in  = filters.DateTimeFilter(field_name="check_in", lookup_expr="lte")

    start_check_out = filters.DateTimeFilter(field_name="check_out", lookup_expr="gte")
    end_check_out = filters.DateTimeFilter(field_name="check_out", lookup_expr="lte")

    is_check_out = filters.BooleanFilter(field_name='is_check_out')
    class Meta:
        model = CheckIn
        exclude = []
