from django import forms

class NewspaperOCRForm(forms.Form):
    image = forms.ImageField(required=True, help_text="Upload the front page image for OCR editorial and date extraction.")
