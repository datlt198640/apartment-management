from typing import List
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.conf import settings
from services.loggers.file_logger import FileLogger
from services.models.repo import Repo
from services.helpers.utils import Utils
from services.sms.speed_sms import SpeedSMS as SMSService
from ..consts import TargetAccount


def get_verif_target_email():
    model = Repo.load(Repo.VARIABLE)
    return model.objects.get_value("VERIF_TARGET_EMAIL")


def get_verif_target_phone_number():
    model = Repo.load(Repo.VARIABLE)
    return model.objects.get_value("VERIF_TARGET_PHONE_NUMBER")


class VerificationTestUtils:
    @staticmethod
    def send(target, code):
        if "@" in str(target):
            return VerificationTestUtils.send_email(target, code)
        return VerificationTestUtils.send_sms(target, code)

    @staticmethod
    def send_email(target, code):
        subject = f"{settings.APP_TITLE} - Mã kích hoạt"
        body = render_to_string(
            "emails/otp.html",
            {"code": code},
        )

        return Utils.send_email(subject, body, target)

    @staticmethod
    def send_sms(target, code):
        message = f"Ma xac thuc SPEEDSMS cua ban la {code}"
        client = SMSService(target, message)
        return client.send_sms()


class VerificationUtils:
    @staticmethod
    def send(target, code, template, extra):
        if "@" in str(target):
            VerificationUtils.send_email(target, code, template, extra)
        else:
            VerificationUtils.send_sms(target, code, template, extra)
        FileLogger.log(target, "verif")

    @staticmethod
    def send_email(target, code, template, extra):
        if fake_target := get_verif_target_email():
            target = fake_target

        subject = "[Vinmec] - Mã kích hoạt"
        if custom_subject := extra.get("subject"):
            subject = custom_subject
        body = render_to_string(
            f"emails/{template}.html",
            {"code": code, "extra": extra},
        )

        Utils.send_email_async(subject, body, target)

    @staticmethod
    def send_sms(target, code):
        if fake_target := get_verif_target_phone_number():
            target = fake_target
        """
        message = " ".join(
            [
                f"{settings.APP_TITLE} - Ma OTP cua quy khach la: {code}.",
                "De dam bao an toan, vui long KHONG chia se OTP cho bat ky ai.",
            ]
        )
        """
        message = f"Ma xac thuc SPEEDSMS cua ban la {code}"
        client = SMSService(target, message)
        client.send_sms_async()


class AfterCreatingAccount:
    @staticmethod
    def send(target, name, account_type=TargetAccount.STAFF):
        if "@" in str(target):
            AfterCreatingAccount.send_email(target, name, account_type)
        else:
            AfterCreatingAccount.send_sms(target, name, account_type)
        FileLogger.log(target, "verif")

    @staticmethod
    def send_email(target, name, account_type):
        if fake_target := get_verif_target_email():
            target = fake_target

        subject = "[Vinmec] "
        subject += (
            "Thông báo khởi tạo tài khoản hệ thống HTKD Doctor Referral Program (DRP)"
        )

        login_url = Utils.get_base_url()
        body = render_to_string(
            f"emails/creating_{account_type}.html",
            {"name": name, "email": target, "login_url": f"{login_url}/login"},
        )

        Utils.send_email_async(subject, body, target)

    @staticmethod
    def send_sms(target, _name, _account_type):
        if fake_target := get_verif_target_phone_number():
            target = fake_target

        login_url = Utils.get_base_url()
        message = " ".join(
            [
                f"Bạn vui lòng vào link {login_url}",
                "và dùng tính năng quên mật khẩu để tạo mật khẩu mới.",
            ]
        )
        client = SMSService(target, message)
        client.send_sms_async()


class VerifModelUtils:
    default_whitelist_code = settings.DEFAULT_WHITELIST_OTP

    def __init__(self, model=None):
        self.model = Repo.load(Repo.VERIF)
        self.verif_log_model = Repo.load(Repo.VERIF_LOG)
        self.whitelist_target_model = Repo.load(Repo.WHITELIST_TARGET)
        self.variable_model = Repo.load(Repo.VARIABLE)

    def get_error_message(self):
        return ("You have entered incorrect OTP so many times. Please try again later")

    def create(self, ips: List[str], target: str, template="otp", extra=None):
        if extra is None:
            extra = {}
        try:
            in_whitelist = self.in_whitelist(target)

            code = Utils.get_random_number()
            uid = Utils.get_uuid()

            if in_whitelist or settings.TESTING:
                code = self.default_whitelist_code

            if not settings.TESTING and not self.write_log(ips, str(target)):
                return (False, self.get_error_message())

            self.model.objects.create(uid=uid, code=code, target=target)

            if in_whitelist or settings.TESTING:
                return (True, uid)

            VerificationUtils.send(target, code, template, extra)

            return (True, uid)
        except Exception as e:
            print(repr(e))
            return (False, self.get_error_message())

    def create_again(self, ips: List[str], uid: str):
        error_message = ("Can not send OTP, please try again after 90 seconds")

        if not uid:
            return (False, error_message)

        item = self.model.objects.filter(uid=uid).order_by("-id").first()

        if not item:
            return (False, error_message)

        in_whitelist = self.in_whitelist(item.target)

        today = datetime.now()
        diff = today - item.updated_at
        diff_seconds = diff.total_seconds()

        if diff_seconds <= settings.VERIFICATION_CODE_EXPIRED_PERIOD:
            return (False, error_message)

        if in_whitelist or settings.TESTING:
            item.code = self.default_whitelist_code
        else:
            item.code = Utils.get_random_number()

        if not self.write_log(ips, item.target):
            return (False, self.get_error_message())

        item.save()

        if in_whitelist or settings.TESTING:
            return (True, item.target)

        VerificationUtils.send(item.target, item.code)

        return (True, item.target)

    def get(self, uid: str, code: str) -> str:
        try:
            if not uid or not code:
                return None

            item = self.model.objects.get(uid=uid, code=code)

            today = datetime.now()
            diff = today - item.updated_at
            diff_seconds = diff.total_seconds()

            if diff_seconds > settings.VERIFICATION_CODE_EXPIRED_PERIOD:
                return None

            return item
        except self.model.DoesNotExist:
            return None

    def in_whitelist(self, target):
        try:
            self.whitelist_target_model.objects.get(target=target)
            return True
        except self.whitelist_target_model.DoesNotExist:
            return False

    def write_log(self, ips: List[str], target: str):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)

        count = self.verif_log_model.objects.filter(
            ips__overlap=ips,
            target=target,
            created_at__gte=start_date,
            created_at__lte=end_date,
        ).count()

        max_count = int(
            self.variable_model.objects.get_value("MAX_OTP_PER_TARGET_PER_DAY", "0")
        )
        if count > max_count:
            return None

        return self.verif_log_model.objects.create(ips=ips, target=target)
