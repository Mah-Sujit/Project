Title: Django File Compression Tool with Unit Tests

```python
# File: compression_tool/views.py

import os
import tempfile
import zipfile
from django.http import HttpResponse
from django.views import View
from django.core.files.uploadedfile import UploadedFile

class FileCompressionView(View):
    """
    Django view to handle file compression requests.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to compress uploaded files into a ZIP archive.
        """
        files = request.FILES.getlist('file')
        if not files:
            return HttpResponse("No files uploaded.", status=400)

        with tempfile.NamedTemporaryFile(delete=True, suffix='.zip') as temp_zip:
            with zipfile.ZipFile(temp_zip, 'w') as zip_archive:
                for file_obj in files:
                    if isinstance(file_obj, UploadedFile):
                        # Write each uploaded file into the zip archive
                        zip_archive.writestr(file_obj.name, file_obj.read())

            # Send the compressed file back as a response
            temp_zip.seek(0)
            response = HttpResponse(temp_zip.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="compressed_files.zip"'
            return response
```

```python
# File: compression_tool/tests.py

from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

class FileCompressionViewTests(TestCase):
    """
    Unit tests for the FileCompressionView.
    """

    def setUp(self):
        """
        Initialize the test client.
        """
        self.client = Client()

    def test_compression_with_single_file(self):
        """
        Test compression with a single file upload.
        """
        file_content = b"Hello, Test!"
        uploaded_file = SimpleUploadedFile("test.txt", file_content)

        response = self.client.post('/compress/', {'file': uploaded_file})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Type'] == 'application/zip')
        self.assertIn(b'test.txt', response.content)

    def test_compression_with_multiple_files(self):
        """
        Test compression with multiple files upload.
        """
        file1_content = b"Hello, World!"
        file2_content = b"Another file content."
        
        uploaded_files = [
            SimpleUploadedFile("hello.txt", file1_content),
            SimpleUploadedFile("another.txt", file2_content)
        ]

        response = self.client.post('/compress/', {'file': uploaded_files})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Type'] == 'application/zip')
        self.assertIn(b'hello.txt', response.content)
        self.assertIn(b'another.txt', response.content)

    def test_compression_with_no_file(self):
        """
        Test compression route with no files upload.
        """
        response = self.client.post('/compress/', {})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"No files uploaded.")
```

```python
# File: compression_tool/urls.py

from django.urls import path
from .views import FileCompressionView

urlpatterns = [
    path('compress/', FileCompressionView.as_view(), name='file_compress'),
]
```

```python
# File: compression_tool/__init__.py

# This is the package initialization file.
```

```python
# File: compression_tool/apps.py

from django.apps import AppConfig

class CompressionToolConfig(AppConfig):
    """
    Configuration for the Compression Tool app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'compression_tool'
```

```python
# Include the compression_tool app in your Django project's settings.py

# File: myproject/settings.py

INSTALLED_APPS = [
    # Other installed apps
    'compression_tool',
]
```

Instructions:
1. Add the compression_tool to your Django project's `INSTALLED_APPS`.
2. Create a URL route to handle file uploads for compression.
3. Use a Django view to compress uploaded files into a ZIP archive.
4. Write unit tests to ensure the tool's functionality is correct.
```