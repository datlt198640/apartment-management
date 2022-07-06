from rest_framework.serializers import ModelSerializer
from ..models import CheckIn
from modules.account.member.models import Member
from modules.account.user.helpers.srs import UserSr
from modules.account.member.helpers.srs import MemberSr, MemberShipSr
from modules.account.member.models import Member, MemberShip


class CheckInSr(ModelSerializer):
    class Meta:
        model = CheckIn
        exclude = ()

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        user = UserSr(obj.member.user).data
        rep["member_email"] = user["email"]
        rep["member_phone_number"] = user["phone_number"]

        member = Member.objects.filter(id = obj.member.id).first()
        membership = MemberShip.objects.filter(member=member).first()

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

