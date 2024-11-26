from django.shortcuts import render, redirect
from .forms import NewspaperOCRForm
from .models import Book, Newspaper
from .ocr_utils import extract_editorial_and_date_from_image

# Create your views here.
from django.shortcuts import render
from .models import Book, Newspaper

def newspaper_ocr_view(request):
    if request.method == 'POST':
        form = NewspaperOCRForm(request.POST, request.FILES)
        if form.is_valid():
            # Perform OCR on the uploaded image
            image = form.cleaned_data['image']
            editorial, date = extract_editorial_and_date_from_image(image)

            # Create a new instance of Newspaper with extracted data
            newspaper = Newspaper(editorial=editorial, date=date)
            newspaper.save()
            return redirect('admin:library_newspaper_changelist')  # Redirect to the newspaper list in admin

    else:
        form = NewspaperOCRForm()

    return render(request, 'newspaper_ocr_form.html', {'form': form})


def welcome(request):
    return render(request, 'library/welcome.html')

def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

def newspaper_list(request):
    newspapers = Newspaper.objects.all()
    return render(request, 'library/newspaper_list.html', {'newspapers': newspapers})
