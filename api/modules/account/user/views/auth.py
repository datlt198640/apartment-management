from drf_spectacular.utils import extend_schema
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

from services.models.repo import Repo
from services.helpers.utils import Utils
from services.helpers.res_utils import ResUtils
from services.helpers.token_utils import TokenUtils

from modules.noti.verif.helpers.model_utils import VerifModelUtils

from modules.account.staff.models import Staff
from modules.account.helpers.model_utils import AccountModelUtils
from ..helpers.srs import LoginSr
from ..helpers.swagger_types import (
    LoginResponseType,
    ChangePwdRequestType,
    ResetPwsRequestType,
    ResetPwsResponseType,
    ResetPwsVerificationRequestType,
)
from modules.account.member.models import Member, Device
from modules.account.member.models import Device
from modules.account.member.helpers.srs import DeviceSr
from modules.account.member.helpers.model_utils import MemberModelUtils

User = Repo.load_user()


class LoginView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=LoginSr,
        responses={200: LoginResponseType},
    )
    def post(self, request, *args, **kwargs):
        if message := Utils.check_captcha(request):
            return ResUtils.err({"detail": message})

        # device_type = request.data.get("type", None)
        # device_member = request.data.get("user", None)
        # device_registration_token = request.data.get("registration_token", "")

        # device_obj = {
        #     "type": device_type,
        #     "member": device_member,
        #     "registration_token": device_registration_token,
        # }
        # Device.objects.filter(member=request.data["member"]).delete()

        # serializer = DeviceSr(data=device_obj)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        error_message = ("Incorrect login information. Please try again")
        serializer = LoginSr(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data["username"].lower()
        password = serializer.data["password"]

        query_field = "email" if "@" in username else "phone_number"
        if query_field == "phone_number":
            username = Utils.phone_to_canonical_format(username)

        condition = {query_field: username}
        try:
            user = User.objects.get(**condition)
            if not user.is_active:
                error_message = ("This user is inactive")
                return ResUtils.err(error_message)

            if check_password(password, user.password):
                token = TokenUtils.generate(user)
                response = ResUtils.jwt_response_handler(token, user, request)
                return ResUtils.res(response)
        except User.DoesNotExist:
            return ResUtils.err(error_message)
        return ResUtils.err(error_message)


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        token = TokenUtils.get_token_from_header(request, False)
        token_context = TokenUtils.get_token_context(request)
        token_signature = TokenUtils.get_token_signature(token)

        if user := User.objects.filter(token_signature=token_signature).first():
            registration_token = request.data.get("registration_token", None)
            if registration_token:
                MemberModelUtils.empty_device_token(
                    user.member, registration_token)
        TokenUtils.revoke(token_context, token_signature)
        return ResUtils.res({})


class ChangePwdView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    @extend_schema(
        request=ChangePwdRequestType,
    )
    def post(self, request, format=None):
        params = self.request.data

        user = self.get_object()

        old_password = params.get("old_password", 0)
        password = params.get("password", "")

        if not old_password or check_password(old_password, user.password) is False:
            return ResUtils.err({"old_password": ("Incorrect current password")})

        if error_msg := Utils.password_validate(password):
            return ResUtils.err({"detail": error_msg})

        user.password = make_password(password)
        user.save()

        return ResUtils.res({})


class ResetPwdView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=ResetPwsRequestType,
        responses={200: ResetPwsResponseType},
    )
    def post(self, request, format=None):
        if message := Utils.check_captcha(request):
            return ResUtils.err({"detail": message})

        username = self.request.data.get("username", "")

        default_response = ResUtils.res(
            {"verif_id": Utils.get_uuid(), "username": Utils.mask_username(username)}
        )

        verif_mu = VerifModelUtils()
        account_mu = AccountModelUtils()
        if not username or not isinstance(username, str):
            return default_response

        user = account_mu.get_user(username)
        if not user:
            return default_response

        name = user.username

        if hasattr(user, "staff"):
            name = user.staff.fullname

        ok, result = verif_mu.create(
            Utils.get_ip_list(request),
            username,
            "reset_password",
            {"subject": "[APTM] Request to reset system password",
                "name": name},
        )

        if ok:
            return ResUtils.res(
                {"verif_id": result, "username": Utils.mask_username(username)}
            )
        return ResUtils.err({"detail": result})


class ResetPwdVerificationView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(request=ResetPwsVerificationRequestType)
    def post(self, request, format=None):
        password = self.request.data.get("password", "")
        verif_id = self.request.data.get("verif_id", "")
        otp_code = self.request.data.get("otp_code", "")

        if error_msg := Utils.password_validate(password):
            return ResUtils.err({"detail": error_msg})

        verif_mu = VerifModelUtils()

        verif = verif_mu.get(verif_id, otp_code)
        if not verif:
            return ResUtils.err({"detail": ("Invalid OTP")})

        try:
            account_mu = AccountModelUtils()
            user = account_mu.get_user(verif.target)
            user.set_password(password)
            user.save()
            return ResUtils.res({})
        except Staff.DoesNotExist:
            return ResUtils.err({"detail": ("Can not reset password")})


class RefreshCheckView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        return ResUtils.res({})


class RefreshView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        token_context = TokenUtils.get_token_context(request)
        token = TokenUtils.get_token_from_header(request, False)
        token_signature = TokenUtils.get_token_signature(token)
        success, result = TokenUtils.refresh(token_context, token_signature)
        if not success:
            return ResUtils.err(result)
        return ResUtils.res({"token": result})
