from django.contrib import admin
from .models import Dish, DishCategory


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "price", "dish_category")

@admin.register(DishCategory)
class DishCategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
