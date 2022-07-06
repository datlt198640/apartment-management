from firebase_admin.exceptions import NotFoundError, InvalidArgumentError
from services.helpers.firebase import Firebase
from modules.account.member.models import Device


class FcmMessage:
    @staticmethod
    def send_to_single_device(device, title, body, data=None):
        if not data:
            data = {}

        firebase = Firebase()
        messaging = firebase.messaging
        registration_token = device.registration_token
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data,
            token=registration_token,
        )
        try:
            messaging.send(message)
            print("Sendding notification")
        except Exception as e:
            print(e)

    @staticmethod
    def send_to_multiple_devices(devices, title, body, data=None):
        """
        This function send a batch of notifications which have the same data to multiple devices
        """
        if not data:
            data = {}
        for device in devices:
            FcmMessage.send_to_single_device(
                device=device, title=title, body=body, data=data
            )
