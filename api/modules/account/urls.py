import os
from django.urls import path, include

app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = (
    path("staff/", include("modules.account.staff.urls", namespace="staff")),
    path("member/", include("modules.account.member.urls", namespace="member")),
    path("role/", include("modules.account.role.urls", namespace="role")),
    path("check-in/", include("modules.account.check_in.urls", namespace="check_in")),
)
