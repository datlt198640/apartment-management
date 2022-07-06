from django.db.models import QuerySet
from services.models.repo import Repo
from .srs import ClubInfoSr


class ClubInfoModelUtils:
    def __init__(self, model=None):
        self.model = Repo.load(Repo.CLUB_INFO)

    def seeding(self, index: int, single: bool = False, save: bool = True) -> QuerySet:

        if index == 0:
            raise Exception("Indext must be start with 1.")

        def get_data(i: int) -> dict:
            data = {
                "title": f"title{i}",
                "description": f"description{i}",
                "content": f"content{i}"
            }
            if save is False:
                return data
            try:
                instance = self.model.objects.get(title=data["title"])
            except self.model.DoesNotExist:
                instance = ClubInfoSr(data=data)
                instance.is_valid(raise_exception=True)
                instance = instance.save()
            return instance

        def get_list_data(index):
            return [get_data(i) for i in range(1, index + 1)]

        return get_data(index) if single is True else get_list_data(index)
