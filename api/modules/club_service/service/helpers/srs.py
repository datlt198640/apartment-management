from django.db.models import Q
from rest_framework.serializers import ModelSerializer
from ..models import Service, ServiceTime, ImageService
from modules.club_service.subservice.helpers.srs import SubserviceSr, SubserviceCategorySr, SubserviceTypeSr
from modules.club_service.subservice.models import Subservice, SubserviceCategory, SubserviceType
from modules.club_service.dish.models import Dish
from modules.club_service.dish.helpers.srs import DishSr, DishCategorySr


class ServiceSr(ModelSerializer):

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        service_time_data = ServiceTimeSr(obj.servicetime).data
        rep["open_time"] = service_time_data["open_time"]
        rep["close_time"] = service_time_data["close_time"]
        rep["image_url"] = []
        rep["subservice_category"] = []
        rep["subservice"] = []
        rep["dish_category"] = []
        rep["dish"] = []
        subservice_type = SubserviceType.objects.filter(service=obj.id).first()
        images = ImageService.objects.filter(service=obj.id)
        for image in images:
            if image:
                rep["image_url"].append(ImageServiceSr(image).data["image_url"])
        if subservice_type:
            rep["subservice_type"] = SubserviceTypeSr(subservice_type).data
            subservice_categories = SubserviceCategory.objects.filter(
                subservice_type=subservice_type.id)
            for subservice_category in subservice_categories:
                if subservice_category:
                    rep["subservice_category"].append(
                        SubserviceCategorySr(subservice_category).data)
                    subservices = Subservice.objects.filter(
                        subservice_category=subservice_category.id)
                    for subservice in subservices:
                        if subservice:
                            rep["subservice"].append(
                                SubserviceSr(subservice).data)

        if obj.dish_categories.all().count() > 0:
            for dish_category in obj.dish_categories.all():
                rep["dish_category"].append(DishCategorySr(dish_category).data)
                dishes = Dish.objects.filter(
                    Q(dish_category=dish_category.id) & Q(service=obj.id))
                for dish in dishes:
                    rep["dish"].append(DishSr(dish).data)
        return rep

    class Meta:
        model = Service
        exclude = ()


class ServiceTimeSr(ModelSerializer):
    class Meta:
        model = ServiceTime
        exclude = ()


class ImageServiceSr(ModelSerializer):
    class Meta:
        model = ImageService
        exclude = ()
