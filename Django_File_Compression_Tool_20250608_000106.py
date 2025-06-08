Title: Django File Compression Tool

```python
# models.py
from django.db import models

class CompressedFile(models.Model):
    original_file = models.FileField(upload_to='uploads/')
    compressed_file = models.FileField(upload_to='compressed/', null=True, blank=True)
    compression_ratio = models.FloatField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compressed {self.original_file.name}"

# views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import CompressedFile
from .forms import FileUploadForm
from .utils import compress_file

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            # Perform compression
            compress_file(instance)
            return HttpResponseRedirect('/success/')
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})

def success(request):
    files = CompressedFile.objects.all()
    return render(request, 'success.html', {'files': files})

# forms.py
from django import forms
from .models import CompressedFile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = CompressedFile
        fields = ['original_file']

# utils.py
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import gzip

def compress_file(instance):
    original_path = instance.original_file.path
    compressed_path = original_path + '.gz'
    
    # Compress the file
    with open(original_path, 'rb') as original_file:
        with gzip.open(compressed_path, 'wb') as compressed_file:
            compressed_file.writelines(original_file)

    # Calculate compression ratio
    original_size = os.path.getsize(original_path)
    compressed_size = os.path.getsize(compressed_path)
    compression_ratio = compressed_size / original_size

    # Save compressed file and ratio
    with open(compressed_path, 'rb') as f:
        file_name = os.path.basename(compressed_path)
        instance.compressed_file.save(file_name, ContentFile(f.read()), save=False)
    
    instance.compression_ratio = compression_ratio
    instance.save()

    # Clean up compressed local file
    os.remove(compressed_path)

# urls.py
from django.urls import path 
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload'),
    path('success/', views.success, name='success'),
]

# upload.html
"""
{% block content %}
  <h2>Upload a new file:</h2>
  <form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Upload</button>
  </form>
{% endblock %}
"""

# success.html
"""
{% block content %}
  <h2>Successful Uploads</h2>
  {% if files %}
    <ul>
      {% for file in files %}
        <li>
          Original File: {{ file.original_file.name }} - 
          Compressed File: {{ file.compressed_file.name }} - 
          Compression Ratio: {{ file.compression_ratio|floatformat:2 }}
        </li>
      {% endfor %}
    </ul>
  {% else %}
    <p>No files have been uploaded yet.</p>
  {% endif %}
{% endblock %}
"""
```

The above code creates a simple Django-based file compression tool following the MVC architecture. It allows users to upload files, which are then compressed using gzip and stored, along with a computed compression ratio. The `CompressedFile` model stores original and compressed files, while views handle uploading and displaying results. Utility function `compress_file` performs the actual file compression.