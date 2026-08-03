
from django.urls import include, path

from account.views import (
    LoginView,
    PasswordEmailUpdateView,
    PostListProfile,
    ProfileUpdateView,
    ProfileView,
    RegisterView,
    logout_view,
)

app_name = "account"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/password_change/<uuid:pk>/", PasswordEmailUpdateView.as_view(), name="profile_change_password"),
    path("profile/my_posts/", PostListProfile.as_view(), name="my_posts"),
    path("profile/edit/<int:pk>/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("api/v1/", include("account.api.v1.urls"), name="account_api"),
]
