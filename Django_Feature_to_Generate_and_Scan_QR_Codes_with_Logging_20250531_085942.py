Title: Django Feature to Generate and Scan QR Codes with Logging

```python
# models.py
from django.db import models

# Model to store QRCode information
class QRCode(models.Model):
    data = models.TextField()
    image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QRCode(id={self.id}, data='{self.data}')"

# views.py
import logging
import os
import qrcode
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import QRCode
from qrtools import QR

# Initialize logger
logger = logging.getLogger(__name__)

# View to generate a QR code
def generate_qr_code(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        # Generate QR code image
        img = qrcode.make(data)
        img_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes', f"{data}.png")
        img.save(img_path)

        # Save QR code info in the database
        qr_code = QRCode(data=data, image=f'qr_codes/{data}.png')
        qr_code.save()

        # Log the QR code generation
        logger.info(f"Generated QR code for data: {data}")

        return redirect('qr_code_detail', qr_code.id)

    return render(request, 'generate_qr.html')

# View to scan a QR code
def scan_qr_code(request, qr_code_id):
    qr_code = get_object_or_404(QRCode, pk=qr_code_id)
    qr = QR(filename=qr_code.image.path)

    if qr.decode():
        # Log the decoded QR code data
        logger.info(f"Scanned QR code with data: {qr.data}")
        return render(request, 'scan_qr.html', {'data': qr.data})
    else:
        logger.error(f"Failed to scan QR code with ID: {qr_code_id}")
        return render(request, 'scan_qr.html', {'error': 'Failed to scan the QR code.'})

# templates/generate_qr.html
'''
<form method="post">
    {% csrf_token %}
    <label for="data">Enter data to generate QR Code:</label>
    <input type="text" id="data" name="data" required>
    <button type="submit">Generate QR Code</button>
</form>
'''

# templates/scan_qr.html
'''
{% if data %}
    <p>Data from QR code: {{ data }}</p>
{% elif error %}
    <p>Error: {{ error }}</p>
{% endif %}
'''

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_qr_code, name='generate_qr'),
    path('scan/<int:qr_code_id>/', views.scan_qr_code, name='qr_code_detail'),
]

# settings.py adjustments for media files
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configure logging
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# Remember to configure your Django application to serve media files during development
# by setting up the MEDIA_URL and MEDIA_ROOT as shown above.
```

This implementation uses the `qrcode` library to generate QR codes and the `qrtools` library to scan them. Logging is used to track QR code generation and scanning activities. Adjust logging configurations as needed for your environment.