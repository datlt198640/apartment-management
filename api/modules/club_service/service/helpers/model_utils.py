from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from services.helpers.utils import Utils
from services.models.repo import Repo
from .srs import ServiceSr, ServiceTimeSr, ImageServiceSr
from ..models import ImageService
from modules.club_service.subservice.models import SubserviceCategory, SubserviceType
from modules.club_service.subservice.helpers.srs import SubserviceCategorySr, SubserviceTypeSr


def add_image(images, service_obj):
    if images:
        for image in images:
            image_obj = {'service': service_obj.pk, 'image_url': image}
            img_sr = ImageServiceSr(data=image_obj)
            img_sr.is_valid(raise_exception=True)
            img_sr.save()


class ServiceModelUtils:
    def __init__(self):
        self.model = Repo.load(Repo.SERVICE)

    def seeding(self, index: int, single: bool = False, save: bool = True) -> QuerySet:
        if index == 0:
            raise Exception("Indext must be start with 1.")

        def get_data(i: int) -> dict:
            data = {"title": f'title{i}'}

            if save is False:
                return data

            try:
                instance = self.model.objects.get(title=data["title"])
            except self.model.DoesNotExist:
                instance = self.create_item(data)
            return instance

        def get_list_data(index):
            return [get_data(i) for i in range(1, index + 1)]

        return get_data(index) if single is True else get_list_data(index)

    def create_item(self, data):
        service_sr = ServiceSr(data=data)
        service_sr.is_valid(raise_exception=True)
        service = service_sr.save()

        data = Utils.update_request_payload(data, dict(service=service.pk))
        sr = ServiceTimeSr(data=data)
        sr.is_valid(raise_exception=True)
        sr.save()

        images = data.get("image_url", [])
        add_image(images, service)

        return service

    def update_item(self, obj, data):
        service_time_sr = ServiceTimeSr(
            obj.servicetime, data=data, partial=True)
        service_time_sr.is_valid(raise_exception=True)
        service_time_sr.save()

        for image in obj.image_service.all():
            item = get_object_or_404(ImageService, pk=image.pk)
            item.delete()
        images = data.get("image_url", [])
        add_image(images, obj)
        sr = ServiceSr(obj, data=data, partial=True)
        sr.is_valid(raise_exception=True)
        return sr.save()

    def get_list_subservice_type(self):
        data = SubserviceType.objects.all()
        srs = SubserviceTypeSr(data, many=True)
        return [{"label": subservice_type["title"], "value":subservice_type["id"]} for subservice_type in srs.data]

    def get_list_subservice_category(self):
        data = SubserviceCategory.objects.all()
        srs = SubserviceCategorySr(data, many=True)
        return [{"label": subservice_type["title"], "value":subservice_type["id"]} for subservice_type in srs.data]
