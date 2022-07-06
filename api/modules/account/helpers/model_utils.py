from services.models.repo import Repo
from services.helpers.utils import Utils

User = Repo.load_user()


class AccountModelUtils:
    def __init__(self, model=None):
        pass

    def get_user(self, username):
        try:
            query_field = "email" if "@" in username else "phone_number"
            if query_field == "phone_number":
                username = Utils.phone_to_canonical_format(username)

            condition = {query_field: username}

            return User.objects.get(**condition)
        except User.DoesNotExist:
            return None
