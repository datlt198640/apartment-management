from rest_framework.serializers import ModelSerializer
from ..models import Dish, DishCategory


class DishSr(ModelSerializer):
    class Meta:
        model = Dish
        exclude = ()
        
class DishCategorySr(ModelSerializer):
    class Meta:
        model = DishCategory
        exclude = ()
