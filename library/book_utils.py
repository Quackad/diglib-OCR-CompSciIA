import cv2
from pyzbar.pyzbar import decode
import isbnlib
import requests
from django.conf import settings

def fetch_book_data_by_isbn(isbn):
    """Fetch book details by ISBN using the Google Books API."""
    api_url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={settings.GOOGLE_BOOKS_API_KEY}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            volume_info = data["items"][0]["volumeInfo"]
            return {
                'title': volume_info.get('title'),
                'author': ', '.join(volume_info.get('authors', [])),
                'isbn': isbn,
                'publication_date': volume_info.get('publishedDate', '')[:10]  # Format date as YYYY-MM-DD
            }
    return None

def is_valid_isbn(isbn):
    """Checks if a given string is a valid ISBN."""
    isbn = isbn.replace("-", "").replace(" ", "")
    return isbnlib.is_isbn13(isbn) or isbnlib.is_isbn10(isbn)

def extract_isbn_from_barcode(image):
    """
    Extracts ISBN from a barcode in an uploaded image.
    
    Args:
        image: An OpenCV image (numpy array) containing a barcode.
        
    Returns:
        str: The detected ISBN, or None if no valid ISBN was found.
    """
    # Decode barcodes from the image
    decoded_objects = decode(image)
    for obj in decoded_objects:
        isbn = obj.data.decode("utf-8")
        if is_valid_isbn(isbn):
            return isbn
    return None
