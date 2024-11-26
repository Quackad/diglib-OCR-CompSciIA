import numpy as np
import cv2
from django.contrib import admin
from django import forms
from django.shortcuts import render, redirect
from django.urls import path, reverse
from .models import Newspaper, Book
from .ocr_utils import extract_editorial_and_date_from_image
from .book_utils import fetch_book_data_by_isbn, extract_isbn_from_barcode

class BookBarcodeForm(forms.Form):
    """Form to upload an image for ISBN barcode scanning."""
    image = forms.ImageField(required=True, help_text="Upload an image of the book's ISBN barcode.")


class BookPreviewForm(forms.ModelForm):
    """Form to preview and confirm scanned book data."""
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publication_date']

# Form to upload image for OCR processing
class NewspaperOCRForm(forms.Form):
    image = forms.ImageField(required=True, help_text="Upload the front page image for OCR editorial and date extraction.")

# Form for preview and confirm step
class NewspaperPreviewForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = ['editorial', 'date']

@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ('editorial', 'date')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add-via-ocr/', self.admin_site.admin_view(self.add_via_ocr), name="add_via_ocr"),
        ]
        return custom_urls + urls
    def add_via_ocr(self, request):
        if request.method == 'POST' and 'preview' in request.POST:
            # Step 1: Handle Image Upload and Perform OCR
            form = NewspaperOCRForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data['image']
                editorial, date = extract_editorial_and_date_from_image(image)

                # Pre-fill the preview form with extracted data
                preview_form = NewspaperPreviewForm(initial={'editorial': editorial, 'date': date})
                return render(request, 'admin/newspaper_ocr_preview.html', {
                    'form': preview_form,
                    'opts': self.model._meta,
                    'title': 'Preview OCR Data',
                })
        
        elif request.method == 'POST' and 'confirm' in request.POST:
            # Step 2: Confirm and Save the Data
            preview_form = NewspaperPreviewForm(request.POST)
            if preview_form.is_valid():
                # Save the validated data to the Newspaper model
                preview_form.save()
                self.message_user(request, "Newspaper added successfully with OCR data.")
                return redirect('admin:library_newspaper_changelist')

        else:
            # Initial form load for image upload
            form = NewspaperOCRForm()

        return render(request, 'admin/newspaper_ocr_form.html', {
            'form': form,
            'opts': self.model._meta,
            'title': 'Add Newspaper via OCR',
        })
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['add_via_ocr_url'] = reverse('admin:add_via_ocr')
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'publication_date')
    change_list_template = "admin/library/book_changelist.html"  # Custom change list template

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add-via-isbn/', self.admin_site.admin_view(self.add_via_isbn), name="add_book_via_isbn"),
        ]
        return custom_urls + urls

    def add_via_isbn(self, request):
        """Handle 'Add Book via ISBN' functionality."""
        if request.method == 'POST':
            form = BookBarcodeForm(request.POST, request.FILES)
            if form.is_valid():
                # Read the uploaded image
                uploaded_file = form.cleaned_data['image']
                image_array = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

                # Extract ISBN from the barcode in the image
                isbn = extract_isbn_from_barcode(image_array)
                if isbn:
                    # Fetch book data using the Google Books API
                    book_data = fetch_book_data_by_isbn(isbn)
                    if book_data:
                        # Prefill the preview form with fetched book data
                        preview_form = BookPreviewForm(initial=book_data)
                        return render(request, 'admin/book_isbn_preview.html', {
                            'form': preview_form,
                            'opts': self.model._meta,
                        })
                    else:
                        self.message_user(request, "No book data found for the scanned ISBN.")
                        return redirect('admin:add_book_via_isbn')
                else:
                    self.message_user(request, "No valid ISBN barcode detected in the image.")
                    return redirect('admin:add_book_via_isbn')
        else:
            form = BookBarcodeForm()

        return render(request, 'admin/book_barcode_form.html', {
            'form': form,
            'opts': self.model._meta,
        })

    def changelist_view(self, request, extra_context=None):
        """Customize the change list view with additional context for buttons."""
        extra_context = extra_context or {}
        extra_context['add_via_isbn_url'] = reverse('admin:add_book_via_isbn')
        return super().changelist_view(request, extra_context=extra_context)