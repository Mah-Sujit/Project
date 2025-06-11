Title: Merging Multiple PDF Files in Django with Unit Tests

```python
# models.py
from django.db import models

class PDFDocument(models.Model):
    document = models.FileField(upload_to='pdfs/')

# utils.py
from PyPDF2 import PdfWriter, PdfReader
from django.core.files.base import ContentFile

def merge_pdfs(pdf_file_list):
    """
    Merges multiple PDF files into a single PDF file.

    Parameters:
    pdf_file_list (list of file-like objects): A list of PDF file-like objects to be merged.

    Returns:
    ContentFile: The merged PDF file as a ContentFile object.
    """
    pdf_writer = PdfWriter()

    # Loop through each PDF in the list and add its pages to the writer
    for pdf_file in pdf_file_list:
        pdf_reader = PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])

    # Create a content file from the writer's data
    output = ContentFile(b'')
    pdf_writer.write(output)
    output.seek(0)

    return output

# tests.py
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .utils import merge_pdfs

class MergePDFsTest(TestCase):
    def setUp(self):
        # Create two simple PDF files for testing
        self.pdf1 = SimpleUploadedFile("file1.pdf", b"%PDF-1.4\n1 0 obj\n<</Type /Catalog>>\nendobj\nxref\n0 1\n0000000000 65535 f\r\ntrailer\n<</Size 1>>\nstartxref\n12\n%%EOF\n")
        self.pdf2 = SimpleUploadedFile("file2.pdf", b"%PDF-1.4\n1 0 obj\n<</Type /Catalog>>\nendobj\nxref\n0 1\n0000000000 65535 f\r\ntrailer\n<</Size 1>>\nstartxref\n12\n%%EOF\n")

    def test_merge_pdfs(self):
        # Merge the PDFs
        merged_pdf = merge_pdfs([self.pdf1, self.pdf2])

        # Check if the result is not None
        self.assertIsNotNone(merged_pdf)

        # Check if the content of the merged PDF is larger than individual PDFs
        self.assertGreater(len(merged_pdf.read()), len(self.pdf1.read()))

        # Verify if the merged PDF file contains two pages
        merged_pdf.seek(0)
        pdf_reader = PdfReader(merged_pdf)
        self.assertEqual(len(pdf_reader.pages), 2)
```

In this code, we define a `PDFDocument` model that represents PDF files in our Django project. The `merge_pdfs` function in `utils.py` takes a list of PDF file-like objects and merges them into a single PDF file. The result is returned as a `ContentFile`. In `tests.py`, we write unit tests using Django's `TestCase` to ensure that the `merge_pdfs` function behaves as expected. These tests check that the merged PDF is not `None`, has greater content size than individual PDFs, and contains the correct number of pages.