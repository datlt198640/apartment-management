import os
from django.urls import path
from .views.crud import SubserviceViewSet
from .views.subservice_category_crud import SubserviceCategoryViewSet
from .views.subservice_type_crud import SubserviceTypeViewSet


def get_subservice_url():
    BASE_ENDPOINT = SubserviceViewSet.as_view(
        {"get": "list", "post": "add", "delete": "delete_list"}
    )

    PK_ENDPOINT = SubserviceViewSet.as_view(
        {"get": "retrieve", "put": "change", "delete": "delete"}
    )


    return [
        path("", BASE_ENDPOINT),
        path("<int:pk>", PK_ENDPOINT),
    ]

def get_subservice_category_url():
    BASE_ENDPOINT = SubserviceCategoryViewSet.as_view(
        {"get": "list", "post": "add", "delete": "delete_list"}
    )

    PK_ENDPOINT = SubserviceCategoryViewSet.as_view(
        {"get": "retrieve", "put": "change", "delete": "delete"}
    )


    return [
        path("category/", BASE_ENDPOINT),
        path("category/<int:pk>", PK_ENDPOINT),
    ]

def get_subservice_type_url():
    BASE_ENDPOINT = SubserviceTypeViewSet.as_view(
        {"get": "list", "post": "add", "delete": "delete_list"}
    )

    PK_ENDPOINT = SubserviceTypeViewSet.as_view(
        {"get": "retrieve", "put": "change", "delete": "delete"}
    )


    return [
        path("type/", BASE_ENDPOINT),
        path("type/<int:pk>", PK_ENDPOINT),
    ]


app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = [] + get_subservice_url() + get_subservice_category_url() + get_subservice_type_url()