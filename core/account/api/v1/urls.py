from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (RegisterApi,
                    AuthTokenApi,
                    JwtAuthToken,
                    DiscardTokenApi,
                    ChangePasswordApi,
                    ProfileApi,
                    VerifyAccountApi)

app_name = "api-v1"
urlpatterns = [
    # Auth urls
    path("register/",
         RegisterApi.as_view(),
         name="register_api"),

    path("change_password/",
         ChangePasswordApi.as_view(),
         name="change_password"),

    # Profile urls
    path("profile/",
         ProfileApi.as_view(),
         name="profile"),

    # Token Base urls
    path("token/login/",
         AuthTokenApi.as_view(),
         name="auth_token"),

    path("token/logout/",
         DiscardTokenApi.as_view(),
         name="discard_token"),

    # JWT Base urls
    path("token/jwt/create/",
         JwtAuthToken.as_view(),
         name="token_obtain_pair"),

    path("token/jwt/refresh/",
         TokenRefreshView.as_view(),
         name="token_refresh"),

    path(
        "token/jwt/verify_account/",
        VerifyAccountApi.as_view(),
        name="account_verify_jwt",
    ),

    path("token/jwt/verify/",
         TokenVerifyView.as_view(),
         name="token_verify"),
]
