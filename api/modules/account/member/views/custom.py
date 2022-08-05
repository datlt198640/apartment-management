from django.conf import settings
from rest_framework.views import APIView
from services.helpers.res_utils import ResUtils
from ..helpers.srs import MemberPermissionSr
from ..helpers.model_utils import MemberModelUtils
from ..helpers.model_utils import MemberModelUtils


class ProfileView(APIView):

    def __init__(self):
        self.member_mu = MemberModelUtils()

    def get_user(self):
        return self.request.user

    def get(self, request, format=None):
        member = self.get_user().member

        data = MemberPermissionSr(member).data

        return ResUtils.res(data)

    def put(self, request, format=None):
        user = self.get_user()
        member = user.member

        data = request.data

        mu = MemberModelUtils()
        obj = mu.update_item(member, data)

        return ResUtils.res(MemberPermissionSr(obj).data)
