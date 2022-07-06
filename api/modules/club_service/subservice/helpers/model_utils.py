from django.db.models import Q
from django.db.models import QuerySet
from django.contrib.auth.models import Group
from services.helpers.utils import Utils
from services.models.repo import Repo
from modules.account.user.helpers.srs import UserSr
from modules.account.helpers.group_srs import GroupSr


class DishModelUtils:
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
                instance = self.model.objects.get(title = data["title"])
            except self.model.DoesNotExist:
                instance = self.create_item(data)
            return instance

        def get_list_data(index):
            return [get_data(i) for i in range(1, index + 1)]

        return get_data(index) if single is True else get_list_data(index)