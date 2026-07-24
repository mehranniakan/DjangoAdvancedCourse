from django.urls import path

from OpenWeather.api.v1.views import OpenWeatherApi

urlpatterns = [
    path("open-weather/", OpenWeatherApi.as_view() , name='open_weather')
]
