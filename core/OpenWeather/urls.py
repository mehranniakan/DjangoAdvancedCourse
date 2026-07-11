from django.urls import path, include

urlpatterns = [
    path('api/v1/', include("OpenWeather.api.v1.urls"), name='api-v1'),
]
