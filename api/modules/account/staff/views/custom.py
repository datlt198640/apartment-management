from rest_framework.views import APIView

from services.helpers.res_utils import ResUtils
from ..helpers.srs import StaffPermissionSr
from ..helpers.model_utils import StaffModelUtils


class ProfileView(APIView):
    def get_user(self):
        return self.request.user

    def get(self, request, format=None):
        staff = self.get_user().staff
        data = StaffPermissionSr(staff).data
        return ResUtils.res(data)

    def put(self, request, format=None):
        user = self.get_user()
        staff = user.staff

        data = request.data

        mu = StaffModelUtils()
        obj = mu.update_item(staff, data)

        return ResUtils.res(StaffPermissionSr(obj).data)
