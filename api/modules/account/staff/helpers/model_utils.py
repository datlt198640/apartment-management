from django.db.models import Q
from django.db.models import QuerySet
from django.contrib.auth.models import Group
from services.helpers.utils import Utils
from services.models.repo import Repo
from modules.account.user.helpers.srs import UserSr
from modules.account.helpers.group_srs import GroupSr
from .srs import StaffSr
from modules.account.helpers.group_srs import GroupSr
from modules.account.user.consts import STAFF_MANAGER


class StaffModelUtils:
    def __init__(self):
        self.model = Repo.load(Repo.STAFF)

    def seeding(self, index: int, single: bool = False, save: bool = True) -> QuerySet:
        group = Group.objects.first()
        if not group:
            group = Group.objects.create(name="g1")
        if index == 0:
            raise Exception("Indext must be start with 1.")

        def get_data(i: int) -> dict:
            phone_number = f"+849066965{i}" if i >= 10 else f"+8490669652{i}"
            test_password = "Qwerty!@#456"
            data = {
                "phone_number": phone_number,
                "email": f"test{i}@gmail.com",
                "password": test_password,
                "fullname": f"fullname {i}",
                "gender": 1,
                "groups": [group.pk],
            }

            if save is False:
                return data

            try:
                instance = self.model.objects.get(
                    Q(user__phone_number=data["phone_number"])
                    | Q(user__email=data["email"])
                )
            except self.model.DoesNotExist:
                instance = self.create_item(data)
            return instance

        def get_list_data(index):
            return [get_data(i) for i in range(1, index + 1)]

        return get_data(index) if single is True else get_list_data(index)

    def create_item(self, data):
        groups = self.get_staff_groups()
        data = Utils.update_request_payload(data, dict(groups=groups))
        user_sr = UserSr(data=data)
        user_sr.is_valid(raise_exception=True)
        user = user_sr.save()

        data = Utils.update_request_payload(data, dict(user=user.pk))
        sr = StaffSr(data=data)
        sr.is_valid(raise_exception=True)

        return sr.save()

    def update_item(self, obj, data):
        user_sr = UserSr(obj.user, data=data, partial=True)
        user_sr.is_valid(raise_exception=True)
        user_sr.save()

        sr = StaffSr(obj, data=data, partial=True)
        sr.is_valid(raise_exception=True)
        return sr.save()

    def get_staff_groups(self) -> list[int]:
        result = Group.objects.filter(name=STAFF_MANAGER).values_list(
            "id", flat=True
        )
        return list(result)

    def get(self, username: str) -> QuerySet:
        return self.model.objects.get(email=username)

    def get_list_group(self) -> list:
        raw_data = GroupSr(Group.objects.all(), many=True).data
        return [{"value": group["id"], "label": group["name"]} for group in raw_data]
