Title: Django Feature for Generating and Scanning QR Codes

```python
# Install necessary packages:
# pip install qrcode[pil] pillow django-qrcode-opencv

# Django settings: Add 'qr_code.apps.QrCodeConfig' to INSTALLED_APPS

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_qr_code, name='generate_qr_code'),
    path('scan/', views.scan_qr_code, name='scan_qr_code'),
]

# views.py
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.uploadedfile import UploadedFile
import qrcode
import cv2
import numpy as np

def generate_qr_code(request):
    """View function for generating a QR code."""
    if request.method == 'POST':
        data = request.POST.get('data', '')
        qr_img = generate_qr(data)
        response = HttpResponse(content_type='image/png')
        qr_img.save(response, 'PNG')
        return response
    return render(request, 'generate_qr_code.html')

def scan_qr_code(request):
    """View function for scanning a QR code."""
    if request.method == 'POST':
        qr_file = request.FILES['qr_file']
        data = scan_uploaded_qr(qr_file)
        return HttpResponse(data)
    return render(request, 'scan_qr_code.html')

def generate_qr(data):
    """Generate a QR code from the given data."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    return qr_img

def scan_uploaded_qr(qr_file: UploadedFile):
    """Scan and decode the QR code from an uploaded image file."""
    file_data = np.frombuffer(qr_file.read(), np.uint8)
    img = cv2.imdecode(file_data, cv2.IMREAD_COLOR)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)
    return data

# generate_qr_code.html
'''
<!DOCTYPE html>
<html>
<body>
    <h2>Generate QR Code</h2>
    <form method="POST">
        {% csrf_token %}
        <label for="data">Data:</label><br>
        <input type="text" id="data" name="data"><br>
        <input type="submit" value="Generate QR">
    </form>
</body>
</html>
'''

# scan_qr_code.html
'''
<!DOCTYPE html>
<html>
<body>
    <h2>Scan QR Code</h2>
    <form method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        <label for="qr_file">Select QR Image:</label><br>
        <input type="file" id="qr_file" name="qr_file"><br>
        <input type="submit" value="Scan QR">
    </form>
</body>
</html>
'''
```
