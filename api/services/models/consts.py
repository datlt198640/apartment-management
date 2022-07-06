class Gender:
    FEMALE = 0
    MALE = 1
    NONE = 2


GENDER_CHOICES = (
    (Gender.NONE, "Không xác định"),
    (Gender.FEMALE, "Nữ"),
    (Gender.MALE, "Nam"),
)

GENDER_DICT = dict(GENDER_CHOICES)

class Remind:
    ONEDAY = 1
    TWODAY = 2
    THREEDAY = 3


REMIND_CHOICES = (
    (Remind.ONEDAY, "Trước một ngày"),
    (Remind.TWODAY, "Trước hai ngày"),
    (Remind.THREEDAY, "Trước ba ngày"),
)

REMIND_DICT = dict(REMIND_CHOICES)

class StatusService:
    DELETED = 1
    READY = 2

STATUS_SERVICE_CHOICES = (
    (StatusService.DELETED, "Đã xóa "),
    (StatusService.READY, "Sẵn sàng "),
)

STATUS_SERVICE_DICT = dict(STATUS_SERVICE_CHOICES)

class ServiceType:
    NONE = 0
    STAY = 1
    CELEBRATE = 2
    ENTERTAIN = 3
    DINE = 4
    SHOP = 5
    RELAX = 6

SERVICE_TYPE_CHOICES = (
    (ServiceType.STAY, "STAY "),
    (ServiceType.CELEBRATE, "CELEBRATE "),
    (ServiceType.ENTERTAIN, "ENTERTAIN "),
    (ServiceType.DINE, "DINE "),
    (ServiceType.SHOP, "SHOP "),
    (ServiceType.RELAX, "RELAX "),
)

TYPE_SERVICE_DICT = dict(SERVICE_TYPE_CHOICES)

