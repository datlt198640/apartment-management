class NotificationType:
    NONE = 0
    SERVICE = 1


NOTIFICATION_TYPE_CHOICES = (
    (NotificationType.NONE, "NONE"),
    (NotificationType.SERVICE, "SERVICE"),
)