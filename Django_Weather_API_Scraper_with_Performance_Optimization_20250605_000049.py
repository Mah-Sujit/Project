Title: Django Weather API Scraper with Performance Optimization

```python
import requests
from django.utils import timezone
from myapp.models import WeatherData

# Define constants for weather API
API_URL = 'https://api.weatherapi.com/v1/current.json'
API_KEY = 'your_api_key_here'  # Replace with your actual API key

def fetch_weather_data(city):
    """
    Fetches weather data for a given city using the Weather API.
    Optimizations: Avoids duplicate requests, handles errors gracefully.
    """
    # Check if we already have a recent record for this city
    recent_data = WeatherData.objects.filter(
        city=city, 
        timestamp__gte=timezone.now() - timezone.timedelta(hours=1)
    ).first()

    if recent_data:
        return recent_data

    response = requests.get(API_URL, params={'key': API_KEY, 'q': city})

    # Process response
    if response.status_code == 200:
        data = response.json()
        weather_data = WeatherData(
            city=city,
            temperature=data['current']['temp_c'],
            condition=data['current']['condition']['text'],
            timestamp=timezone.now()
        )
        weather_data.save()
        return weather_data
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# models.py for storing weather data
from django.db import models

class WeatherData(models.Model):
    """
    Model to store weather data in the database.
    """
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    condition = models.CharField(max_length=100)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Weather in {self.city} at {self.timestamp}: {self.temperature}°C, {self.condition}"
```

This code provides a simple Django feature to scrape weather data from a given API and store it in the database. It looks for recent records to avoid unnecessary API calls, optimizing performance. Adjust the code to fit the actual structure of your Django project and insert the real API key for execution.