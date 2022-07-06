from typing import Union
import base64
import json
import requests
from django.conf import settings
from services.helpers.utils import Utils, async_task


class SpeedSMS:
    def __init__(self, target: Union[str, list[str]], message: str):
        self.target = target
        self.message = message

    def __format_phone_number(self, phone_number) -> str:
        if not Utils.check_valid_phone_number(phone_number):
            return ""
        return phone_number[1:]

    def __format_target(self, target: Union[str, list[str]]) -> list[str]:
        result = []

        if isinstance(target, str):
            target = [target]

        for i in target:
            if phone_number := self.__format_phone_number(i):
                result.append(phone_number)
        return result

    def send_sms(self) -> str:
        target = self.__format_target(self.target)
        if not target:
            return False, f"Invalid target: {target}"

        branch_name = settings.SPEED_SMS["BRANCH_NAME"]
        token = "{}:x".format(settings.SPEED_SMS["ACCESS_TOKEN"])
        token = base64.b64encode(token.encode())
        token = token.decode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic {}".format(token),
        }
        url = "https://api.speedsms.vn/index.php/sms/send/"
        data = {
            "to": target,
            "content": self.message,
            "sms_type": settings.SPEED_SMS["TYPE"],
            "sender": branch_name,
        }
        print(data)
        try:
            response = requests.post(url, data=json.dumps(data), headers=headers)
            result = response.json()
            message = str([response.status_code, result])
            if response.status_code == 200 and result["status"] == "success":
                return True, message
            return False, message
        except Exception as e:
            return False, str(repr(e))

    @staticmethod
    @async_task
    def send_sms_async(self, *args):
        return self.send_sms(*args)
