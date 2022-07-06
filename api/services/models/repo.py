import importlib


class Repo:
    USER = ("modules.account.user.models", "User")
    GROUP = ("django.contrib.auth.models", "Group")
    STAFF = ("modules.account.staff.models", "Staff")
    MEMBER = ("modules.account.member.models", "Member")
    VARIABLE = ("modules.configuration.variable.models", "Variable")

    CLUB_INFO = ("modules.infomation.club_info.models", "ClubInfo")
    PROMOTION = ("modules.infomation.promotion.models", "Promotion")

    SERVICE = ("modules.club_service.service.models", "Service")

    EVENT = ("modules.event.event.models", "Event")

    VERIF = ("modules.noti.verif.models", "Verif")
    NOTIFICATION = ("modules.noti.notification.models", "Notification")

    WHITELIST_TARGET = ("modules.noti.verif.models", "WhitelistTarget")

    @staticmethod
    def load(module_tuple):
        return getattr(importlib.import_module(module_tuple[0]), module_tuple[1])

    @staticmethod
    def load_user():
        return Repo.load(Repo.USER)
