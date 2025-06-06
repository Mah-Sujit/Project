Title: Django Feature for Generating and Scanning QR Codes

```python
# Install required packages:
# pip install django qrcode[pil] pillow qrcode-reader

from django.shortcuts import render
from django.http import JsonResponse
import qrcode
from qrcode.image.pil import PilImage
from io import BytesIO
from base64 import b64encode
from qrcode_reader import read_qr_code

# Function to generate a QR code from input data
def generate_qr_code(data):
    # QRCode object initialization; optimized configurations
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to the QRCode object
    qr.add_data(data)
    qr.make(fit=True)
    
    # Generate QR code image
    img = qr.make_image(fill='black', back_color='white', image_factory=PilImage)
    
    # Save QR code to a buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    # Encode the QR code image into a base64 string
    img_str = b64encode(buffer.getvalue()).decode()
    return img_str

# Function to scan and extract data from a QR code
def scan_qr_code(image_file):
    # Read QR code using qrcode-reader
    data, points = read_qr_code(image_file)
    
    # Return the data if QR code is decoded
    if data:
        return data
    else:
        return "No valid QR code found."

# View function for handling QR code generation
def qr_code_view(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        data = request.POST.get('data')
        
        # Generate QR code
        qr_code_img_str = generate_qr_code(data)
        
        # Return JSON response with base64 encoded image
        return JsonResponse({'qr_code': qr_code_img_str})

    return render(request, 'qr_code.html')

# View function for handling QR code scanning
def scan_qr_view(request):
    if request.method == 'POST' and request.FILES.get('qr_image'):
        # Get the uploaded image from the POST request
        qr_image = request.FILES['qr_image']
        
        # Extract data from the QR code
        extracted_data = scan_qr_code(qr_image)
        
        # Return JSON response with extracted data
        return JsonResponse({'data': extracted_data})

    return render(request, 'scan_qr.html')
```

**Note:**

1. Integrate `qr_code_view` and `scan_qr_view` into your Django application by defining appropriate URL patterns in `urls.py`.
2. Ensure templates `qr_code.html` and `scan_qr.html` are created for rendering the respective input forms and user interfaces.
3. Modify the QR code scanning and rendering logic if needed based on your application requirements.