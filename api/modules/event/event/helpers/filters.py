from django_filters import rest_framework as filters
from ..models import EventMember


class EventMemberFilter(filters.FilterSet):

    event_title = filters.CharFilter(field_name="event__title", lookup_expr="icontains")

    class Meta:
        model = EventMember
        exclude = []
