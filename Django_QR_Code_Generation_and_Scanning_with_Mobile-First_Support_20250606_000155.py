Title: Django QR Code Generation and Scanning with Mobile-First Support

```python
# models.py
from django.db import models
import qrcode  # Library for generating QR codes
from io import BytesIO
from django.core.files import File

class QRCode(models.Model):
    data = models.TextField()
    qr_image = models.ImageField(upload_to='qr_codes/', blank=True)

    def save(self, *args, **kwargs):
        # Generate QR code image
        qr = qrcode.make(self.data)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        # Save image to field
        self.qr_image.save(f'qr_{self.id}.png', File(buffer), save=False)
        super().save(*args, **kwargs)

# forms.py
from django import forms

class QRCodeForm(forms.ModelForm):
    class Meta:
        model = QRCode
        fields = ['data']
        widgets = {
            'data': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter data for QR code',
                'required': True,
            }),
        }

# views.py
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import QRCode
from .forms import QRCodeForm

class QRCodeCreateView(CreateView):
    model = QRCode
    form_class = QRCodeForm
    template_name = 'qr_code_form.html'
    success_url = reverse_lazy('qr_code_list')  # URL name for QR code list view

# urls.py
from django.urls import path
from .views import QRCodeCreateView

urlpatterns = [
    path('create/', QRCodeCreateView.as_view(), name='qr_code_create'),
]

# qr_code_form.html
'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> <!-- Mobile-first support -->
    <title>Create QR Code</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-4">
        <h1>Create QR Code</h1>
        <form method="post" enctype="multipart/form-data">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary">Generate QR Code</button>
        </form>
    </div>
</body>
</html>
'''
```

This feature allows users to generate QR codes by entering data into a form. To support mobile-first design, the template uses Bootstrap for responsive design elements. Users can generate QR codes via the `/create/` endpoint.