import os
from django.urls import path
from .views.crud import ClubInfoViewSet
from .views.custom import ContactUsView


BASE_ENDPOINT = ClubInfoViewSet.as_view(
    {"get": "list", "post": "add", "delete": "delete_list"}
)

PK_ENDPOINT = ClubInfoViewSet.as_view(
    {"get": "retrieve", "put": "change", "delete": "delete"}
)

app_name = os.getcwd().split(os.sep)[-1]
urlpatterns = [
    path("contact-us", ContactUsView.as_view(), name="contact-us"),
    path("", BASE_ENDPOINT),
    path("<int:pk>", PK_ENDPOINT),
]
