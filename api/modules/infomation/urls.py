import os
from django.urls import path, include

app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = (
    path("club/", include("modules.infomation.club_info.urls", namespace="club_info")),
    path("promotions/", include("modules.infomation.promotion.urls", namespace="promotion")),
)
