Title: QR Code Generation and Scanning in Django

```python
# Import necessary libraries
import qrcode
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.base import ContentFile
import cv2  # OpenCV for QR code scanning
import numpy as np
from django.core.files.uploadedfile import InMemoryUploadedFile

# Function to generate a QR code
def generate_qr_code(request, data):
    """
    Generates a QR code for the given data.
    
    Args:
        request (HttpRequest): The HTTP request object.
        data (str): The data to encode in the QR code.
        
    Returns:
        HttpResponse: An HTTP response containing the QR code image.
    """
    # Create a QR code object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code instance
    img = qr.make_image(fill='black', back_color='white')

    # Save the image to a BytesIO stream
    byte_io = ContentFile(b'')
    img.save(byte_io, format='PNG')

    # Return the image as an HTTP response
    return HttpResponse(byte_io.getvalue(), content_type='image/png')


# Function to scan a QR code
def scan_qr_code(request):
    """
    Scans a QR code from an uploaded image.
    
    Args:
        request (HttpRequest): The HTTP request object which must include an uploaded image file.
        
    Returns:
        HttpResponse: An HTTP response containing the decoded data from the QR code.
    """
    if request.method == 'POST' and request.FILES['qr_image']:
        # Retrieve the uploaded image file
        qr_image = request.FILES['qr_image']
        
        # Read image file into OpenCV format
        file_bytes = np.asarray(bytearray(qr_image.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Initialize QR code detector
        detector = cv2.QRCodeDetector()

        # Detect and decode the QR code
        data, vertices_array, _ = detector.detectAndDecode(img)

        if vertices_array is not None:
            # If a QR code is detected
            return HttpResponse(f'Decoded data: {data}')
        else:
            return HttpResponse('No QR code detected')

    else:
        # In case of GET request or no file uploaded
        return render(request, 'upload_qr.html')


# views.py file where the above functions are defined should be properly wired in urls.py
```

In your templates, you would need an `upload_qr.html` file with a form for uploading images:

```html
<!-- upload_qr.html -->
<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    <input type="file" name="qr_image" accept="image/*">
    <button type="submit">Scan QR Code</button>
</form>
```

This code defines two main functions, `generate_qr_code` for generating QR codes with given data, and `scan_qr_code` for decoding data from uploaded QR code images. The `qr_code` library is used for generating QR codes, while OpenCV is employed to scan and decode QR codes from images.