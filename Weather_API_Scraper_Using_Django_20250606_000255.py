Title: Weather API Scraper Using Django

```python
import requests
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Scrapers weather information from an external API.'

    def handle(self, *args, **kwargs):
        """
        Entry point for the Django management command.
        This function fetches weather data from a specified API
        and displays the results in the console.
        """
        try:
            # Define the URL of the weather API
            api_url = "http://api.openweathermap.org/data/2.5/weather"
            # Define your API key (replace 'YOUR_API_KEY' with an actual API key)
            api_key = "YOUR_API_KEY"
            # Define the city for which weather information is requested
            city = "London"
            # Define query parameters including the city and API key
            params = {
                'q': city,
                'appid': api_key,
                'units': 'metric'  # Use metric system for temperature
            }

            # Make an API GET request to fetch weather data
            response = requests.get(api_url, params=params)
            
            # Raise an exception for HTTP errors
            response.raise_for_status()
            
            # Parse the JSON response from the API
            weather_data = response.json()

            # Access and print specific weather information
            print(f"Weather in {weather_data['name']}:")
            print(f"Temperature: {weather_data['main']['temp']}°C")
            print(f"Weather: {weather_data['weather'][0]['description']}")

        except requests.exceptions.HTTPError as http_err:
            # Print HTTP error statements if received
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            # Handle any other exceptions that may occur
            print(f"An error occurred: {err}")
```

To use this script in a Django project:

1. Ensure you have the `requests` library installed using `pip install requests`.
2. Save the code in a file inside a Django app's `management/commands` directory, e.g., `myapp/management/commands/scrape_weather.py`.
3. Run the script via Django's management command: `python manage.py scrape_weather`.

*Note*: Replace `'YOUR_API_KEY'` with an actual API key obtained from a weather API provider, such as OpenWeatherMap.