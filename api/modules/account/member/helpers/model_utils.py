import os
from django.db.models import Q
from django.db.models import QuerySet
from django.contrib.auth.models import Group
from services.helpers.utils import Utils
from services.models.repo import Repo
from modules.account.user.helpers.srs import UserSr
from modules.account.helpers.group_srs import GroupSr
from modules.account.user.consts import MEMBER_GROUP
from .srs import MemberSr, MemberShipSr, MemberShipTypeSr
from ..models import Member, Device, MemberShipType
from modules.club_service.service.models import Service
from modules.club_service.service.helpers.srs import ServiceSr
import pymssql


server = os.environ.get("REMOTE_DB_SERVER")
user = os.environ.get("REMOTE_DB_MEMBER_USER")
password = os.environ.get("REMOTE_DB_MEMBER_PASSWORD")
database = os.environ.get("REMOTE_DB_MEMBER_DATABASE")


class MemberModelUtils:
    def __init__(self):
        self.model = Repo.load(Repo.MEMBER)

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
                "full_name": f"full_name {i}",
                "dob":  f"2001-01-{i}",
                "occupation": f"occupation {i}",
                "address": f"address {i}",
                "gender": 1,
                "type": 1,
                "register_date": f"2022-01-{i}",
                "expire_date": f"2022-01-{i}",
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
        groups = self.get_member_groups()
        data = Utils.update_request_payload(data, dict(groups=groups))
        user_sr = UserSr(data=data)
        user_sr.is_valid(raise_exception=True)
        user = user_sr.save()

        data = Utils.update_request_payload(data, dict(user=user.pk))
        member_sr = MemberSr(data=data)
        member_sr.is_valid(raise_exception=True)
        member = member_sr.save()

        # data = Utils.update_request_payload(data, dict(member=member.pk))
        data.update(dict(member=member.pk))
        membership_sr = MemberShipSr(data=data)
        membership_sr.is_valid(raise_exception=True)
        membership_sr.save()

        return member

    def update_item(self, obj, data):
        user_sr = UserSr(obj.user, data=data, partial=True)
        user_sr.is_valid(raise_exception=True)
        user_sr.save()

        member_sr = MemberSr(obj, data=data, partial=True)
        member_sr.is_valid(raise_exception=True)
        member = member_sr.save()

        membership_sr = MemberShipSr(obj.membership, data=data, partial=True)
        membership_sr.is_valid(raise_exception=True)
        membership_sr.save()
        return member

    def get_member_groups(self) -> list:
        result = Group.objects.filter(name=MEMBER_GROUP).values_list(
            "id", flat=True
        )
        return list(result)

    def get(self, username: str) -> QuerySet:
        return self.model.objects.get(email=username)

    def get_list_membership_type(self) -> list:
        membership_type = MemberShipType.objects.all()
        membership_type_srs = MemberShipTypeSr(membership_type, many=True)
        return [{"value": data["id"], "label": data["title"]} for data in membership_type_srs.data]

    def get_list_group(self) -> list:
        raw_data = GroupSr(Group.objects.all(), many=True).data
        return [{"value": group["id"], "label": group["name"]} for group in raw_data]

    def get_list_member(self) -> list:
        members = Member.objects.all()
        member_srs = MemberSr(members, many=True).data
        return [{"label": member["full_name"], "value": member["id"]} for member in member_srs]

    def get_list_service(self) -> list:
        services = Service.objects.all()
        service_srs = ServiceSr(services, many=True).data
        return [{"label": service["title"], "value": service["id"]} for service in service_srs]

    @staticmethod
    def empty_device_token(member: QuerySet, registration_token: str):
        Device.objects.filter(member=member).delete()
        Device.objects.filter(registration_token=registration_token).delete()
