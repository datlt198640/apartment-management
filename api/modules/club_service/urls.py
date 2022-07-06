import os
from django.urls import path, include

app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = (
    path("service/", include("modules.club_service.service.urls", namespace="service")),
    path("dish/", include("modules.club_service.dish.urls", namespace="dish")),
    path("subservice/", include("modules.club_service.subservice.urls", namespace="subservice")),
)
