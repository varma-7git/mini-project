from django.urls import path

from .api_views import (
    register_api,
    login_api
)


urlpatterns = [

    path(
        "register/",
        register_api,
        name="register_api"
    ),

    path(
        "login/",
        login_api,
        name="login_api"
    ),

]