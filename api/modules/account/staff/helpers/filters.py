from django_filters import rest_framework as filters
from ..models import Staff


class StaffFilter(filters.FilterSet):
    # vinmec_site = filters.NumberFilter(field_name="vinmec_sites__id")
    # group = filters.NumberFilter(field_name="user__groups__id")

    class Meta:
        model = Staff
        exclude = [
            # "gender",
            "created_at",
            # "fullname",
            "updated_at",
            # "user",
            # "vinmec_sites",
        ]
