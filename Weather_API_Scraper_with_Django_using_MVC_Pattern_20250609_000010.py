Title: Weather API Scraper with Django using MVC Pattern

```python
# views.py
from django.http import JsonResponse
from django.views import View
from .models import WeatherData
from .services import WeatherAPIService

class WeatherAPIView(View):
    def get(self, request, *args, **kwargs):
        """GET request handler to fetch and return weather data"""
        city = request.GET.get('city', 'San Francisco') # Default to San Francisco if no city is provided
        weather_data = WeatherAPIService.fetch_weather(city) # Use service to fetch weather data
        return JsonResponse(weather_data)

# models.py
from django.db import models

class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    condition = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.city}: {self.temperature}°C, {self.condition}'

# services.py
import requests

class WeatherAPIService:
    @staticmethod
    def fetch_weather(city):
        """Fetches weather data from an external weather API"""
        # Example URL. Replace with actual weather API endpoint and key.
        api_key = 'your_api_key'
        url = f'https://api.example.com/weather?city={city}&apikey={api_key}'
        
        try:
            response = requests.get(url)
            response.raise_for_status() # Raise HTTPError for bad responses
            data = response.json() # Convert response to JSON
            
            # Parse required data
            temperature = data['main']['temp']
            condition = data['weather'][0]['description']

            # Log or save the data using the model
            WeatherData.objects.update_or_create(
                city=city,
                defaults={'temperature': temperature, 'condition': condition}
            )
            
            return {
                'city': city,
                'temperature': temperature,
                'condition': condition
            }
        except requests.exceptions.RequestException as e:
            # Handle requests exceptions
            return {'error': str(e)}

# urls.py
from django.urls import path
from .views import WeatherAPIView

urlpatterns = [
    path('api/weather/', WeatherAPIView.as_view(), name='weather_api'),
]

# Run migrations to create WeatherData model in the database
# $ python manage.py makemigrations
# $ python manage.py migrate
```

This code snippet demonstrates a basic weather API scraper using Django, adhering to the MVC pattern. The `views.py` handles requests and responses, the `models.py` defines the data structure, and the `services.py` performs the business logic of fetching weather data from an external API. This separation of concerns offers a clean and scalable approach.