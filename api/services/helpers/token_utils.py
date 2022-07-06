import hashlib
from django.db.models import QuerySet
from django.conf import settings
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from services.models.repo import Repo
from services.helpers.utils import Utils

User = Repo.load_user()


class TokenUtils:
    revoked_status = "REVOKED"

    @staticmethod
    def get_test_fp() -> str:
        return "395fb184305a022fe98eab14c8328d21"

    @staticmethod
    def get_test_user_agent() -> str:
        return " ".join(
            [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)",
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
            ]
        )

    @staticmethod
    def get_token_from_header(request, is_jwt=True):
        prefix = "JWT "
        if not is_jwt:
            prefix = "bearer "

        token_header = request.META.get("HTTP_AUTHORIZATION")

        if not token_header:
            return ""

        if not token_header.startswith(prefix):
            return ""

        return token_header.split(prefix)[-1]

    @staticmethod
    def get_token_context(request) -> str:
        if settings.TESTING:
            fp = TokenUtils.get_test_fp()
            user_agent = TokenUtils.get_test_user_agent()
        else:
            fp = request.META.get("HTTP_FINGERPRINT", "")
            user_agent = str(request.META["HTTP_USER_AGENT"])
        user_agent_hash = hashlib.md5(user_agent.encode("utf-8")).hexdigest()
        return f"{fp}{user_agent_hash}"

    @staticmethod
    def get_token_signature(token: str) -> str:
        return token.split(".")[-1]

    @staticmethod
    def parse(token: str) -> QuerySet:
        try:
            return (
                VerifyJSONWebTokenSerializer()
                .validate({"token": token})
                .get("user", None)
            )
        except Exception:
            return None

    @staticmethod
    def generate_test_token(extended_user: QuerySet) -> str:
        token = TokenUtils.generate(extended_user.user)
        token_context = TokenUtils.get_token_context({})
        token_signature = TokenUtils.get_token_signature(token)
        TokenUtils.update_token_meta_data(
            extended_user.user, token_context, token_signature
        )
        return token

    @staticmethod
    def generate(user: QuerySet) -> str:
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        return jwt_encode_handler(payload)

    @staticmethod
    def revoke(token_context: str, token_signature) -> bool:
        user = User.objects.filter(
            token_context=token_context, token_signature=token_signature
        ).first()

        if not user:
            return False

        user.token_signature = ""
        user.save()
        return True

    @staticmethod
    def is_revoked(token_context: str, token_signature: str) -> bool:
        if not token_context or not token_signature:
            return True

        user = User.objects.filter(
            token_context=token_context, token_signature=token_signature
        ).first()
        return not bool(user)

    @staticmethod
    def update_token_meta_data(
        user: QuerySet, token_context: str, token_signature: str
    ):
        user.token_context = token_context
        user.token_signature = token_signature
        user.token_refresh_limit = Utils.shift_from_now(
            "minutes", settings.JWT_REFRESH_EXPIRATION_DELTA
        )
        user.save()

    @staticmethod
    def refresh(token_context: str, token_signature: str) -> str:
        user = User.objects.filter(
            token_context=token_context, token_signature=token_signature
        ).first()

        if not user:
            return (False, "User does not exist")
        if not user.is_active:
            return (False, "This user is inactive")
        if user.token_refresh_limit < Utils.now():
            return (False, "Invalid refresh limit")

        token = TokenUtils.generate(user)
        token_signature = TokenUtils.get_token_signature(token)

        TokenUtils.update_token_meta_data(user, token_context, token_signature)

        return (True, token)

    @staticmethod
    def generate_from_username(username: str):
        try:
            user = User.objects.get(username=username)
            return user, TokenUtils.generate(user)
        except Exception:
            return None, ""
