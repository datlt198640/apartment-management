class NotiStatus:
    NONE = 0
    EIGHT_DAYS = 1
    TWO_DAYS = 2
    ZERO_DAYS = 3

NotiStatusChoices = (
    (NotiStatus.NONE, "NONE"),
    (NotiStatus.EIGHT_DAYS, "8 Days"),
    (NotiStatus.TWO_DAYS, "2 Days"),
    (NotiStatus.ZERO_DAYS, "Today"),
)