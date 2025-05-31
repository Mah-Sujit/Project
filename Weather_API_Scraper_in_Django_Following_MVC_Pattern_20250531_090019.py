Title: Weather API Scraper in Django Following MVC Pattern

```python
# Install necessary libraries
# pip install requests

# models.py
from django.db import models

class Weather(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.city} - {self.temperature}°C - {self.description}'

# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Weather
from django.views.decorators.csrf import csrf_exempt
import requests

# Replace 'your_api_key' with an actual API key from a weather service provider
API_KEY = 'your_api_key'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric'

def fetch_weather_data(city):
    try:
        response = requests.get(BASE_URL.format(city=city, key=API_KEY))
        data = response.json()
        if response.status_code == 200:
            temperature = data['main']['temp']
            description = data['weather'][0]['description']
            return temperature, description
        else:
            return None, None
    except Exception as e:
        return None, None

@csrf_exempt
def get_weather(request, city_name):
    temperature, description = fetch_weather_data(city_name)
    if temperature is not None and description is not None:
        weather_record = Weather(city=city_name, temperature=temperature, description=description)
        weather_record.save()
        return JsonResponse({'city': city_name, 'temperature': temperature, 'description': description}, status=200)
    else:
        return JsonResponse({'error': 'Unable to fetch weather data'}, status=500)

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('weather/<str:city_name>/', views.get_weather, name='get_weather'),
]

# To utilize this code:
# - Start a new Django project and application.
# - Include these snippets in the relevant files in your Django app.
# - Ensure that you've set up the Django app correctly, and run the server.
# - Access the weather data by visiting /weather/CITY_NAME/ endpoint with a valid weather service API key.
```

This Django feature example consists of a `Weather` model to store weather data, a view function to fetch data from an external weather API and store it, and Django URLs to handle requests. This implementation separates responsibilities, following the Model-View-Controller (MVC) design pattern.