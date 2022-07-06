import zeep
from abc import ABC, abstractmethod
from django.conf import settings
from services.helpers.utils import Utils, async_task

sms_providers_settings = "SMS_PROVIDERS"


class SMSClient(ABC):
    provider_name = ""

    def __init__(self, receiver, message):
        self.receiver = Utils.phone_to_local_format(str(receiver))
        self.message = message
        self.sms_providers = self.get_sms_providers()
        self.data_settings = self.get_data_settings()

    @abstractmethod
    def send_sms(self, **kwargs):
        """
        :param receiver: phone number
        :param message: text
        :return: status code
        """
        pass

    def get_data_settings(self):
        if self.provider_name not in self.sms_providers:
            raise Exception(
                "Doesn't exist provider name {} in {}".format(
                    self.provider_name, sms_providers_settings
                )
            )
        return self.sms_providers[self.provider_name]

    def get_sms_providers(self):
        if not hasattr(settings, sms_providers_settings):
            raise Exception(
                "You must configure '{}' in settings".format(sms_providers_settings)
            )
        return getattr(settings, sms_providers_settings)


class AZTechSMS(SMSClient):
    provider_name = "aztech"

    def send_sms(self, **kwargs):
        if settings.SMS_ENABLE is not True or settings.TESTING:
            return
        wsdl = self.data_settings["wsdl"]
        # order of items in params is important
        params = [
            self.data_settings["auth_username"],
            self.data_settings["auth_password"],
            self.data_settings["brand_name"],
            self.message,
            self.receiver,
            self.data_settings["sms_type"],
        ]

        client = zeep.Client(wsdl=wsdl)
        return client.service.sendSms(*params)

    @async_task
    def send_sms_async(self, *args):
        self.send_sms(*args)
