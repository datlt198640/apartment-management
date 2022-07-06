import os
from django.urls import path
from .views.crud import CheckInViewSet


def get_check_in_url():
    BASE_ENDPOINT = CheckInViewSet.as_view(
        {"get": "list", "post": "add", "delete": "delete_list"}
    )

    PK_ENDPOINT = CheckInViewSet.as_view(
        {"get": "retrieve", "put": "change", "delete": "delete"}
    )


    return [
        path("", BASE_ENDPOINT),
        path("<int:pk>", PK_ENDPOINT),
    ]


app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = [] + get_check_in_url()