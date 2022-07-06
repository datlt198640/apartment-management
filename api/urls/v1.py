import os
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView


app_name = os.getcwd().split(os.sep)[-1]
urlpatterns = (
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="api_v1:schema"),
        name="swagger-ui",
    ),
    path("auth/", include("modules.account.user.urls", namespace="auth")),
    path("noti/", include("modules.noti.urls", namespace="noti")),
    path("account/", include("modules.account.urls", namespace="account")),

    path("infomation/", include("modules.infomation.urls", namespace="infomation")),
    path("services/", include("modules.club_service.urls", namespace="services")),
    path("event/", include("modules.event.urls", namespace="event")),

    path(
        "configuration/",
        include("modules.configuration.urls", namespace="configuration"),
    ),
)
