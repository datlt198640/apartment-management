import os
from django.urls import path
from .views.auth import (
    LoginView,
    RefreshView,
    RefreshCheckView,
    LogoutView,
    ResetPwdView,
    ResetPwdVerificationView,
    ChangePwdView,
)


app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    path("refresh-check/", RefreshCheckView.as_view(), name="refresh_check"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("reset-pwd/", ResetPwdView.as_view(), name="resetPassword"),
    path(
        "reset-pwd-verification/",
        ResetPwdVerificationView.as_view(),
        name="reset_pwd_verification",
    ),
    path("change-pwd/", ChangePwdView.as_view(), name="changePassword"),
]
