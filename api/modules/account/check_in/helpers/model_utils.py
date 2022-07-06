from django.db.models import QuerySet
from services.models.repo import Repo
from modules.account.member.models import Member
from modules.account.member.helpers.srs import MemberSr
from modules.account.user.models import User
from modules.account.user.helpers.srs import UserSr
from modules.account.member.models import Member, MemberShipType
from modules.account.member.helpers.srs import MemberSr, MemberShipTypeSr


class CheckInModelUtils:
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

    def get_list_member(self):
        members = Member.objects.all()
        return MemberSr(members, many=True).data

    def get_list_member_label(self):
        queryset = Member.objects.all()
        members = MemberSr(queryset, many=True).data
        return [{"label": member["full_name"], "value": member["id"]} for member in members]

    def get_list_membership_type(self) -> list :
        membership_type = MemberShipType.objects.all()
        membership_type_srs = MemberShipTypeSr(membership_type, many=True)
        return [{"value": data["id"], "label": data["title"]} for data in membership_type_srs.data]