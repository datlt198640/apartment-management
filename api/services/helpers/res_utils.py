from django.contrib.auth.models import Permission, update_last_login
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from services.helpers.token_utils import TokenUtils
from modules.account.user.helpers.model_utils import UserModelUtils


class ResUtils:
    @staticmethod
    def get_permissions(user=None):
        if user is not None:
            return [item.split(".")[1] for item in user.get_all_permissions()]

        permissions = Permission.objects.all()
        return list(permissions.values_list("codename", flat=True))

    @staticmethod
    def jwt_response_handler(token, user=None, request=None):

        try:
            token_context = TokenUtils.get_token_context(request)
            token_signature = TokenUtils.get_token_signature(token)

            account_type, data = ResUtils.get_account_data(user)

            TokenUtils.update_token_meta_data(user, token_context, token_signature)

            update_last_login(None, user)

            data["permissions"] = UserModelUtils.get_permissions(user)
            data["is_manager"] = UserModelUtils.is_manager(user)

            data["account_type"] = account_type
            data["token"] = token
            return data
        except Exception as e:
            print(repr(e))
            error_message = ("This user didn't associate with any profile.")
            raise ValidationError({"detail": error_message})

    def get_account_data(user):
        from modules.account.staff.helpers.srs import StaffRetrieveSr

        account_type = ""
        if hasattr(user, "staff"):
            account = user.staff
            account_type = "staff"
            return account_type, StaffRetrieveSr(account).data
        return "", {}

    @staticmethod
    def get_token(headers):
        result = headers.get("Authorization", None)
        if result:
            return result.split(" ")[1]
        return ""

    @staticmethod
    def error_format(data):
        if isinstance(data, str):
            return {"detail": [data]}
        if isinstance(data, dict):
            return data
        return {}

    @staticmethod
    def res(item=None, extra=None, **kwargs):
        if item is None:
            item = {}
        if extra is not None:
            item["extra"] = extra
        return Response(item, **kwargs)

    @staticmethod
    def err(data, status_code=status.HTTP_400_BAD_REQUEST):
        return Response(ResUtils.error_format(data), status=status_code)

    @staticmethod
    def error_response_to_string(error_response: dict) -> list:
        result = []
        for _status, value in error_response.items():
            if isinstance(value, str) is True and value:
                result.append(value)
            if isinstance(value, list) is True and value:
                result += value
        return result


JWT_RESPONSE_HANDLER = ResUtils.jwt_response_handler
