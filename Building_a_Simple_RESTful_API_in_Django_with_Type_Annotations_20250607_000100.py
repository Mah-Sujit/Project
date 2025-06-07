Title: Building a Simple RESTful API in Django with Type Annotations

```python
# Import necessary modules and functions from Django and DRF (Django Rest Framework)
from django.urls import path
from django.http import JsonResponse, HttpRequest
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from typing import Union, Dict

# Define a simple view using Django's View class
class SimpleApiView(APIView):
    # Respond to GET requests
    def get(self, request: HttpRequest) -> Response:
        # Return a simple JSON response
        data: Dict[str, str] = {"message": "Hello, world!"}
        return Response(data, status=status.HTTP_200_OK)

    # Respond to POST requests
    def post(self, request: HttpRequest) -> Response:
        # Extract data from the request
        incoming_data: Dict[str, Union[str, int]] = request.data
        
        # Check if 'name' is in the request data
        if 'name' in incoming_data:
            response_data: Dict[str, str] = {"message": f"Hello, {incoming_data['name']}!"}
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            # Return a bad request response if 'name' is not provided
            error_data: Dict[str, str] = {"error": "Name is required"}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

# Define a function-based view for simple GET request
@api_view(['GET'])
def simple_function_view(request: HttpRequest) -> Response:
    # Return a simple JSON response
    data: Dict[str, str] = {"message": "Hello from function view!"}
    return Response(data, status=status.HTTP_200_OK)

# Define URL patterns for the API views
urlpatterns = [
    path('api/simple/', SimpleApiView.as_view(), name='simple_api_view'),
    path('api/function-view/', simple_function_view, name='simple_function_view'),
]
```

The code above sets up a basic RESTful API using Django and Django Rest Framework (DRF). Two endpoints are created:

1. A class-based API view (`SimpleApiView`) that handles both GET and POST requests.
2. A function-based API view (`simple_function_view`) that only handles GET requests.

Each view uses type annotations to specify the expected types for input parameters and return values. This not only improves code readability but also helps with static type checking.