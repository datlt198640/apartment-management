from django.core.management.base import BaseCommand
from modules.configuration.variable.models import Variable
from datetime import datetime
from services.helpers.fcm_message import FcmMessage
from ...models import Event, EventMember
from modules.account.member.models import Device
from modules.noti.notification.models import Notification


UID = "DATE_SEND_NOTI_EVENT"


class Command(BaseCommand):
    help = "cmd_event_notification_push"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Start..."))

        now = datetime.now()
        events = Event.objects.filter(start_time__gte=now)
        dates = Variable.objects.get_value(UID)
        list_date = dates.split(",")
        for event in events:
            event_bookings = EventMember.objects.filter(event = event.pk)
            for event_booking in event_bookings:
                member_devices = Device.objects.filter(member = event_booking.member.id)  
                diff = event.start_time - now
                for date in list_date:
                    if diff.days == int(date):
                        for member_device in member_devices:              
                            device = member_device
                            title = "Event"
                            body = f"Event {event.title} is comming after {diff.days} days"
                            FcmMessage().send_to_single_device(device, title, body)
                        Notification.objects.create(title=title, body=body, member=event_booking.member)

        self.stdout.write(self.style.SUCCESS("Done!!!"))
