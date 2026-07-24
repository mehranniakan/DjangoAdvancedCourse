from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from functions import get_weather
from .serializers import OpenWeatherSerializer
from rest_framework.views import APIView


class OpenWeatherApi(GenericAPIView):
    serializer_class = OpenWeatherSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lat = serializer.validated_data["lat"]
        lng = serializer.validated_data["lng"]

        weather_data = get_weather(lat, lng)

        return Response({
            'location': f"{weather_data['sys']['country']} - {weather_data['name']}",
            'sky_situation': weather_data['weather'][0]['description'],
            'temperature': f"{weather_data['main']['temp']} C",
            'feels_like': f"{weather_data['main']['feels_like']} C",
            'humidity': f"{weather_data['main']['humidity']} %",
            'wind_speed': f"{weather_data['wind']['speed']} km/h",
            'wind_direction': f"{weather_data['wind']['deg']} deg",
        }, status=status.HTTP_200_OK)