import os
from django.urls import path
from .views.crud import DishViewSet
from .views.dish_category_crud import DishCategoryViewSet


def get_dish_url():
    BASE_ENDPOINT = DishViewSet.as_view(
        {"get": "list", "post": "add", "delete": "delete_list"}
    )

    PK_ENDPOINT = DishViewSet.as_view(
        {"get": "retrieve", "put": "change", "delete": "delete"}
    )


    return [
        path("", BASE_ENDPOINT),
        path("<int:pk>", PK_ENDPOINT),
    ]

def get_dish_category_url():
    BASE_ENDPOINT = DishCategoryViewSet.as_view(
        {"get": "list", "post": "add", "delete": "delete_list"}
    )

    PK_ENDPOINT = DishCategoryViewSet.as_view(
        {"get": "retrieve", "put": "change", "delete": "delete"}
    )


    return [
        path("category/", BASE_ENDPOINT),
        path("category/<int:pk>", PK_ENDPOINT),
    ]


app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = [] + get_dish_url() + get_dish_category_url()