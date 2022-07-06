import os
from django.urls import path
from .views.crud import EventViewSet
from .views.event_member_crud import EventMemberViewSet

def get_event_url():

    BASE_ENDPOINT = EventViewSet.as_view(
        {"get": "list", "post": "add", "delete": "delete_list"}
    )

    PK_ENDPOINT = EventViewSet.as_view(
        {"get": "retrieve", "put": "change", "delete": "delete"}
    )
    return [
        path("", BASE_ENDPOINT),
        path("<int:pk>", PK_ENDPOINT),
    ]


def get_event_member_url():

    BASE_ENDPOINT = EventMemberViewSet.as_view(
        {"get": "list", "post": "add", "delete": "delete_list"}
    )

    PK_ENDPOINT = EventMemberViewSet.as_view(
        {"get": "retrieve", "put": "change", "delete": "delete"}
    )
    return [
        path("booking/", BASE_ENDPOINT),
        path("booking/<int:pk>", PK_ENDPOINT),
    ]

app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = [] + get_event_url() + get_event_member_url()
