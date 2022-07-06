from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from services.models.repo import Repo
from modules.configuration.variable.helpers.model_utils import VariableModelUtils
from modules.account.staff.helpers.model_utils import StaffModelUtils
from modules.account.user.consts import GROUP_NAMES


User = Repo.load_user()


class Command(BaseCommand):
    help = "cmd_account_seeding"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Start..."))
        password = "Qwerty!@#456"
        # Create super user
        try:
            user = User.objects.create_user(
                username="admin",
                phone_number="+84987654321",
                email="",
                password=password,
            )
            user.is_staff = True
            user.is_superuser = True
            user.save()
        except Exception:
            pass

        # Create group
        for group_name in GROUP_NAMES:
            Group.objects.get_or_create(name=group_name)

        # Set permisison
        permissions = Permission.objects.all()
        for group in Group.objects.all():
            group.permissions.set(permissions)

        # Generate staffs
        staff_list = [
            {
                "email": "staff1@gmail.com",
                "phone_number": "+84901111111",
                "password": password,
                "gender": 1,
                "fullname": "staff1",
                "groups": [Group.objects.get(name=GROUP_NAMES[0]).pk],
            },
        ]
        staff_mu = StaffModelUtils()
        for data in staff_list:
            staff_mu.create_item(data)

        def print_variable_result(uid: str, value: str):
            self.stdout.write(self.style.SUCCESS(f"[+] Variable: {uid}: {value}"))

        # Generate variable
        variable_mu = VariableModelUtils()
        variable_mu.settings_seeding(print_variable_result)

        self.stdout.write(self.style.SUCCESS("Done!!!"))
