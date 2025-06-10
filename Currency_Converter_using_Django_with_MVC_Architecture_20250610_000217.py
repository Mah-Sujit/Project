Title: Currency Converter using Django with MVC Architecture

```python
# Import necessary modules
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import requests

# Model: Currency conversion logic encapsulated in a function
def convert_currency(amount, from_currency, to_currency):
    try:
        # Fetch exchange rate data from an external API
        response = requests.get("https://api.exchangerate-api.com/v4/latest/" + from_currency)
        data = response.json()
        
        # Calculate the converted amount using the exchange rate
        rate = data['rates'][to_currency]
        converted_amount = amount * rate
        
        return converted_amount
    except Exception as e:
        # Handle exceptions and return a failure message
        return str(e)

# View: Rendering the interface and processing requests
class CurrencyConverterView(View):

    def get(self, request):
        # Render a simple form to input amount, from_currency, to_currency
        return render(request, 'currency_converter.html')
    
    def post(self, request):
        # Extract form data from the request
        amount = float(request.POST.get('amount'))
        from_currency = request.POST.get('from_currency')
        to_currency = request.POST.get('to_currency')

        # Convert currency using the model logic
        converted_amount = convert_currency(amount, from_currency, to_currency)
        
        # Return a JSON response with the converted amount
        return JsonResponse({"converted_amount": converted_amount})

# Template: currency_converter.html
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Currency Converter</title>
</head>
<body>
    <h1>Currency Converter</h1>
    <form method="POST">
        {% csrf_token %}
        <label for="amount">Amount:</label>
        <input type="number" step="0.01" name="amount" required><br>
        
        <label for="from_currency">From:</label>
        <input type="text" name="from_currency" value="USD" required><br>
        
        <label for="to_currency">To:</label>
        <input type="text" name="to_currency" value="EUR" required><br>
        
        <button type="submit">Convert</button>
    </form>
    <div id="result"></div>
    
    <script>
        // Capture form submission to dynamically show results
        document.querySelector('form').onsubmit = async function(event) {
            event.preventDefault();
            let formData = new FormData(event.target);
            
            // Send the form data using POST request
            const response = await fetch('', {
                method: 'POST',
                body: formData
            });
            
            // Extract JSON data from the response
            const data = await response.json();
            document.getElementById('result').textContent = 'Converted Amount: ' + data.converted_amount;
        };
    </script>
</body>
</html>
"""

# Define URL in urls.py
from django.urls import path
from .views import CurrencyConverterView

urlpatterns = [
    path('convert/', CurrencyConverterView.as_view(), name='currency_converter'),
]
```

Note:
1. The code uses an external API to get currency exchange rates.
2. Ensure that you have the necessary setup for Django middleware and routes for this to function.
3. Replace the API endpoint and key as per the actual API you're using, and handle API limits and errors appropriately.
4. In a production environment, security measures like rate limiting and API key management should be considered.