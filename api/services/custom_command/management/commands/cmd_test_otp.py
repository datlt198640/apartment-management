from django.core.management.base import BaseCommand
from modules.noti.verif.helpers.model_utils import VerificationTestUtils


class Command(BaseCommand):
    help = "cmd_test_otp"

    def add_arguments(self, parser):
        parser.add_argument("target", type=str, help="Email or phone_number")

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("[+] Start..."))

        target = options.get("target")
        self.stdout.write(self.style.SUCCESS(f"[*] Sending email to: {target}"))
        result = VerificationTestUtils.send(target, "123456")
        print(result)
        self.stdout.write(self.style.SUCCESS("[+] Done!!!"))
