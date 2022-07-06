class Member:
    WELLNESS= 2
    NORMAL = 1
    NONE = 0

MEMBER_CHOICES = (
    (Member.NONE, "None"),
    (Member.NORMAL, "Member"),
    (Member.WELLNESS, "Wellness member"),
)

MEMBER_DICT = dict(MEMBER_CHOICES)

class BookingStatus:
    NONE = 0
    READY = 1

BOOKING_STATUS_CHOICES = (
    (BookingStatus.NONE, "NONE "),
    (BookingStatus.READY, "READY "),
)

BOOKING_STATUS_DICT = dict(BOOKING_STATUS_CHOICES)

class DeviceType:
    IOS = 0
    ANDROID = 1


DEVICE_TYPE_CHOICES = (
    (DeviceType.IOS, "IOS "),
    (DeviceType.ANDROID, "ANDROID "),
)

DEVICE_TYPE_DICT = dict(DEVICE_TYPE_CHOICES)

