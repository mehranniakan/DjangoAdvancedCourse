import requests
from celery import shared_task
from django.core.cache import cache


@shared_task
def get_weather(lat=31.3183, lng=48.6706):
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'lat': lat,
        'lon': lng,
        'units': 'metric',
        'appid': '3dd602f347eb28e75bed50d50a5bd634'
    }
    response = requests.get(base_url, params).json()
    cache.set(f'weather_{lat}_{lng}', response, timeout=20 * 60)
    return response
