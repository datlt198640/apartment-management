import os
from django.urls import path
from .views.crud import ServiceViewSet
from .views.custom import ExploreView


def get_service_url():
    BASE_ENDPOINT = ServiceViewSet.as_view(
        {"get": "list", "post": "add", "delete": "delete_list"}
    )

    PK_ENDPOINT = ServiceViewSet.as_view(
        {"get": "retrieve", "put": "change", "delete": "delete"}
    )

    return [
        path("", BASE_ENDPOINT),
        path("<int:pk>", PK_ENDPOINT),
    ]


app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = [
    path("explore", ExploreView.as_view(), name="explore")
] + get_service_url()
