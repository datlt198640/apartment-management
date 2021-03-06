import os
from django.urls import path, include

app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = (
    path("verif/", include("modules.noti.verif.urls", namespace="verif")),
    path("notification/", include("modules.noti.notification.urls", namespace="notification"))    
)
