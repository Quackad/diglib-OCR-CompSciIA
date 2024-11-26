import cv2
import numpy as np
import matplotlib.pyplot as plt
from pyzbar.pyzbar import decode
import requests

GOOGLE_BOOKS_API_KEY = 'AIzaSyAgXzjRBPfDQaIaaZJcUv1dRcb0ScTKgxk'

def fetch_book_data_by_isbn(isbn):
    """Fetch book details by ISBN using the Google Books API."""
    api_url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={GOOGLE_BOOKS_API_KEY}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            volume_info = data["items"][0]["volumeInfo"]
            return {
                'title': volume_info.get('title', 'Unknown Title'),
                'author': ', '.join(volume_info.get('authors', ['Unknown Author'])),
                'publication_date': volume_info.get('publishedDate', 'Unknown Date')
            }
    return None

def preprocess_image(image_path):
    # Load image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Resize the image to improve detection accuracy
    img = cv2.resize(img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    
    # Apply Gaussian blur to reduce noise
    img_blur = cv2.GaussianBlur(img, (3, 3), 0)
    
    # Apply adaptive thresholding for better edge definition
    img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Sharpen the image
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img_sharp = cv2.filter2D(img_thresh, -1, sharpen_kernel)
    
    # Display the image for inspection
    plt.imshow(img_sharp, cmap='gray')
    plt.title('Preprocessed Image for Barcode Detection')
    plt.axis('off')
    plt.show()
    
    return img_sharp

def scan_barcode(image_path):
    # Read the original image
    original_img = cv2.imread(image_path)
    
    # Try decoding the barcode from the processed image
    processed_img = preprocess_image(image_path)
    decoded_objects_processed = decode(processed_img)
    
    if decoded_objects_processed:
        # If a barcode is found in the processed image, handle it
        for obj in decoded_objects_processed:
            isbn = obj.data.decode("utf-8")
            print("Detected ISBN Barcode (Processed Image):", isbn)
            
            # Fetch book data using the ISBN API
            book_data = fetch_book_data_by_isbn(isbn)
            if book_data:
                print("Book Information Found:")
                print("Title:", book_data['title'])
                print("Author(s):", book_data['author'])
                print("Publication Date:", book_data['publication_date'])
            else:
                print("No book information found for this ISBN.")
        return  # Exit after successful processing
    
    # If no barcode is found in the processed image, try the original image
    print("No barcode detected in processed image. Trying original image...")
    decoded_objects_unprocessed = decode(original_img)
    
    if decoded_objects_unprocessed:
        # If a barcode is found in the original image, handle it
        for obj in decoded_objects_unprocessed:
            isbn = obj.data.decode("utf-8")
            print("Detected ISBN Barcode (Original Image):", isbn)
            
            # Fetch book data using the ISBN API
            book_data = fetch_book_data_by_isbn(isbn)
            if book_data:
                print("Book Information Found:")
                print("Title:", book_data['title'])
                print("Author(s):", book_data['author'])
                print("Publication Date:", book_data['publication_date'])
            else:
                print("No book information found for this ISBN.")
    else:
        print("No barcode detected in either processed or original image.")

# Test with one of the uploaded images
scan_barcode("isbn5.png")  # Update this path as needed
