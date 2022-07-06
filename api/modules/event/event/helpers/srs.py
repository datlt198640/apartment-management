from rest_framework.serializers import ModelSerializer
from ..models import Event, EventMember, ImageEvent
from modules.account.user.helpers.srs import UserSr
from modules.account.member.helpers.srs import MemberSr, MemberShipSr
from modules.account.member.models import Member, MemberShip
class EventSr(ModelSerializer):
    class Meta:
        model = Event
        exclude = ()

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        rep["image_url"] = []
        images = ImageEvent.objects.filter(event=obj.id)
        for image in images:
            if image:
                rep["image_url"].append(ImageEventSr(image).data["image_url"])

        return rep

class ImageEventSr(ModelSerializer):
    class Meta:
        model = ImageEvent
        exclude = ()

class EventMemberSr(ModelSerializer):
    class Meta:
        model = EventMember
        exclude = ()

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        rep = super().to_representation(obj)
        member = Member.objects.filter(id = obj.member.id).first()
        membership = MemberShip.objects.filter(member=member).first()

        rep["event_start_time"] = EventSr(obj.event, partial=True).data["start_time"]
        rep["event_end_time"] = EventSr(obj.event, partial=True).data["end_time"]

        rep["member_real_name"] = MemberSr(member).data["full_name"]
        rep["member_real_phone_number"] = UserSr(member.user).data["phone_number"]
        rep["member_real_email"] = MemberSr(member).data["email"]
        rep["dob"] = MemberSr(member).data["dob"]
        rep["occupation"] = MemberSr(member).data["occupation"]
        rep["address"] = MemberSr(member).data["address"]
        rep["gender"] = MemberSr(member).data["gender"]
        rep["avatar"] = MemberSr(member).data["avatar"]
        rep["membership_type"] = MemberShipSr(membership).data["membership_type"]
        rep["register_date"] = MemberShipSr(membership).data["register_date"]
        rep["expire_date"] = MemberShipSr(membership).data["expire_date"]

        return rep
