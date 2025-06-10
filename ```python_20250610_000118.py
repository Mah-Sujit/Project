```python
# Title: Simple File Compression Tool in Django

import os
import gzip
import shutil
from django.http import HttpResponse
from django.views import View
from django.conf import settings

class FileCompressionView(View):
    """
    A Django view for compressing files using gzip.
    Optimized for performance by reading and writing large blocks.
    """

    def get(self, request, *args, **kwargs):
        # Retrieve the file path from the request
        file_path = request.GET.get('file_path', None)

        if not file_path:
            return HttpResponse("File path not provided.", status=400)
        
        # Ensure the file exists
        if not os.path.exists(file_path):
            return HttpResponse("File does not exist.", status=404)
        
        # Compress the file
        compressed_file_path = self.compress_file(file_path)
        
        # Return the path to the compressed file
        return HttpResponse(f"Compressed file created at: {compressed_file_path}", status=200)
    
    def compress_file(self, file_path):
        """
        Compresses the specified file using gzip.

        Args:
            file_path (str): The path to the file to compress.

        Returns:
            str: The path to the compressed file.
        """
        compressed_file_path = f"{file_path}.gz"

        # Use a large block size for reading/writing for better performance
        block_size = 128 * 1024  # 128 KB

        with open(file_path, 'rb') as original_file:
            with gzip.open(compressed_file_path, 'wb') as compressed_file:
                shutil.copyfileobj(original_file, compressed_file, length=block_size)

        return compressed_file_path

# Example configuration for the Django URL dispatcher to add the file compression route
from django.urls import path

urlpatterns = [
    path('compress-file/', FileCompressionView.as_view(), name='compress-file'),
]
```

This code snippet defines a simple Django view that can compress files using the gzip format. It includes basic error handling and uses a larger block size during file operations to enhance performance. The file paths should be managed with care to handle sensitive data appropriately in production environments.