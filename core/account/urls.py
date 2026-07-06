from django.urls import path, include

from . import views
app_name = 'account'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/v1/', include('account.api.v1.urls'), name='account_api'),
]
