from modules.noti.verif.helpers.model_utils import AfterCreatingAccount
from modules.noti.verif.consts import TargetAccount


class StaffSignals:
    @staticmethod
    def pre_save(*args, **kwargs):
        pass

    @staticmethod
    def post_save(*args, **kwargs):
        created = kwargs.get("created", False)
        if created:
            obj = kwargs.get("instance")
            target = obj.user.email or obj.user.phone_number
            name = obj.fullname
            AfterCreatingAccount.send(target, name, TargetAccount.STAFF)

    @staticmethod
    def pre_delete(*args, **kwargs):
        pass

    @staticmethod
    def post_delete(*args, **kwargs):
        pass
