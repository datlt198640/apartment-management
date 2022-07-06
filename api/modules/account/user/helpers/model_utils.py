from django.contrib.auth.models import Permission
from modules.account.member.models import Member

MANAGER_STAFF = "manager"
MEMBER = "member"
GROUP_NAME = "Manager"


class UserModelUtils:
    @staticmethod
    def get_permissions(user):
        if user.is_staff:
            permissions = Permission.objects.all()
            return list(permissions.values_list("codename", flat=True))
        groups = user.groups.all()
        result = []
        for group in groups:
            for pem in group.permissions.all():
                result.append(pem.codename)
        return result
        # return [item.split(".")[1] for item in user.get_all_permissions()]

    @staticmethod
    def is_manager(user):
        return user.groups.filter(name=GROUP_NAME).exists()

    @staticmethod
    def is_manager_group(group):
        return bool(group.permissions.filter(codename=MANAGER_STAFF).first())

    @staticmethod
    def is_member(user):
        member = Member.objects.filter(user=user.id).first()
        return bool(member)

    @staticmethod
    def is_member_group(group):
        return bool(group.permissions.filter(codename=MEMBER).first())
