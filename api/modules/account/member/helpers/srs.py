from django.db.models import Q
from rest_framework.serializers import ModelSerializer
from modules.account.user.helpers.model_utils import UserModelUtils
from ..models import Member, MemberShip, MemberShipType, BookingService, Device
from modules.account.user.helpers.srs import UserSr
from modules.club_service.service.helpers.srs import ServiceSr
from modules.noti.notification.models import Notification
from django.http.request import QueryDict
from rest_framework.serializers import ValidationError


Model = Member


class BookingServiceSr(ModelSerializer):
    class Meta:
        model = BookingService
        exclude = ()

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        member = Member.objects.filter(id=obj.member.id).first()
        membership = MemberShip.objects.filter(member=member).first()

        rep["member_real_name"] = MemberSr(member).data["full_name"]
        rep["member_real_phone_number"] = UserSr(
            member.user).data["phone_number"]
        rep["member_real_email"] = MemberSr(member).data["email"]
        rep["dob"] = MemberSr(member).data["dob"]
        rep["occupation"] = MemberSr(member).data["occupation"]
        rep["address"] = MemberSr(member).data["address"]
        rep["gender"] = MemberSr(member).data["gender"]
        rep["avatar"] = MemberSr(member).data["avatar"]
        rep["membership_type"] = MemberShipSr(
            membership).data["membership_type"]
        rep["register_date"] = MemberShipSr(membership).data["register_date"]
        rep["expire_date"] = MemberShipSr(membership).data["expire_date"]

        return rep


class MemberSr(ModelSerializer):
    class Meta:
        model = Model
        exclude = []

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        rep["phone_number"] = UserSr(obj.user).data["phone_number"]
        rep["email"] = UserSr(obj.user).data["email"]
        rep["membership_type"] = MemberShipTypeSr(
            obj.membership.membership_type).data
        rep["register_date"] = MemberShipSr(
            obj.membership).data["register_date"]
        rep["expire_date"] = MemberShipSr(obj.membership).data["expire_date"]
        return rep


class MemberShipSr(ModelSerializer):
    class Meta:
        model = MemberShip
        exclude = []


class MemberShipTypeSr(ModelSerializer):
    class Meta:
        model = MemberShipType
        exclude = []


class DeviceSr(ModelSerializer):
    class Meta:
        model = Device
        exclude = []


class MemberRetrieveSr(MemberSr):
    class Meta(MemberSr.Meta):
        exclude = [
            "created_at",
            "updated_at",
            "user",
        ]

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        rep["membership_type"] = MemberShipSr(
            obj.membership).data["membership_type"]
        return rep


class MemberPermissionSr(MemberRetrieveSr):
    class Meta(MemberRetrieveSr.Meta):
        pass

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        is_not_read = Notification.objects.filter(
            Q(member=obj) & Q(is_read=False))
        rep["unread_notification"] = bool(is_not_read)

        rep["phone_number"] = UserSr(obj.user).data["phone_number"]
        rep["email"] = UserSr(obj.user).data["email"]
        rep["membership_type"] = MemberShipTypeSr(
            obj.membership.membership_type).data
        rep["list_services"] = []
        rep["register_date"] = MemberShipSr(
            obj.membership).data["register_date"]
        rep["expire_date"] = MemberShipSr(obj.membership).data["expire_date"]
        rep["permissions"] = UserModelUtils.get_permissions(obj.user)
        # for service in obj.membership.membership_type.services.all():
        #     rep["list_services"].append(ServiceSr(service).data)
        return rep


class MemberOptionSr(MemberSr):
    class Meta(MemberSr.Meta):
        exclude = []

    def to_representation(self, obj):
        groups = obj.user.groups.all()
        return {
            "value": obj.id,
            "label": obj.full_name,
            "email": obj.user.email,
            "phone_number": str(obj.user.phone_number),
            "groups": groups.values_list("id", flat=True),
            "group_labels": groups.values_list("name", flat=True),
        }
