from django.core.management.base import BaseCommand
from services.helpers.fcm_message import FcmMessage


class Command(BaseCommand):
    help = "cmd_test_noti_push"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("[+] Start..."))
        token = "eFhuo4ZRTPKJSDVmOrPYHL:APA91bEtYzAyB_zWZAhF_mjsi9e4psRga_aFFMjZShs6WtpTJ_pKIRliqNPpZy9U8W6P5_2CFf1xQvB_cqwX75-nsOpD70IFiUsFZ5_uCA4SqKQd0aRLpu6ORgZhk5_fZIE2o2fUIf2w"
        title = "test push"
        body = "body of test push"
        FcmMessage().send_to_single_device(token, title, body)
        self.stdout.write(self.style.SUCCESS("[+] Finish..."))
