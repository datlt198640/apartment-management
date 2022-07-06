import os
from django.urls import path
from .views.crud import MemberViewSet
from .views.custom import ProfileView
from .views.membership_type_crud import MemberShipTypeViewSet
from .views.booking import BookingServiceViewSet
from .views.device_crud import DeviceViewSet


def get_member_url():
    BASE_ENDPOINT = MemberViewSet.as_view(
        {"get": "list", "post": "add", "delete": "delete_list"}
    )

    PK_ENDPOINT = MemberViewSet.as_view(
        {"get": "retrieve", "put": "change", "delete": "delete"}
    )

    return [
        path("", BASE_ENDPOINT),
        path("<int:pk>", PK_ENDPOINT),
    ]

def get_membership_type_url():
    BASE_ENDPOINT = MemberShipTypeViewSet.as_view(
        {"get": "list", "post": "add", "delete": "delete_list"}
    )

    PK_ENDPOINT = MemberShipTypeViewSet.as_view(
        {"get": "retrieve", "put": "change", "delete": "delete"}
    )

    return [
        path("membership-type/", BASE_ENDPOINT),
        path("membership-type/<int:pk>", PK_ENDPOINT),
    ]


def get_booking_service_url():
    BASE_ENDPOINT = BookingServiceViewSet.as_view(
        {"get": "list", "post": "add", "delete": "delete_list"}
    )

    PK_ENDPOINT = BookingServiceViewSet.as_view(
        {"get": "retrieve", "put": "change", "delete": "delete"}
    )

    return [
        path("booking-service/", BASE_ENDPOINT),
        path("booking-service/<int:pk>", PK_ENDPOINT),
    ]


def get_device_url():
    BASE_ENDPOINT = DeviceViewSet.as_view(
        {"get": "list", "post": "add"}
    )

    PK_ENDPOINT = DeviceViewSet.as_view(
        {"delete": "delete"}
    )

    return [
        path("device/", BASE_ENDPOINT),
        path("device/<str:registration_token>", PK_ENDPOINT),
    ]


app_name = os.getcwd().split(os.sep)[-1]
urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile")
] + get_member_url() + get_membership_type_url() + get_booking_service_url() + get_device_url()
