import cv2
import pytesseract
import numpy as np
from datetime import datetime
import re


# Preprocess the image for OCR
def preprocess_image(img, scale_factor=2.0):
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Upscale the image to increase OCR accuracy
    upscaled_img = cv2.resize(gray, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
    
    # Apply contrast adjustment to make text stand out more
    contrast_img = cv2.convertScaleAbs(upscaled_img, alpha=1.5, beta=20)
    
    # Apply sharpening filter to enhance text clarity
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened_img = cv2.filter2D(contrast_img, -1, sharpen_kernel)
    
    # Apply binary thresholding for clear text boundaries
    _, binary_img = cv2.threshold(sharpened_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return binary_img

# Perform OCR on the uploaded image and extract the editorial and date
def extract_editorial_and_date_from_image(uploaded_file):
    # Read the image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    # Preprocess the image
    processed_img = preprocess_image(img)

    # General OCR for the date and other text
    text = pytesseract.image_to_string(processed_img)

    # Custom OCR configuration to focus on editorial names
    custom_config = "--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    text2 = pytesseract.image_to_string(processed_img, config=custom_config)
    print("Detected Text 1:", text)
    print("Detected Text 2:", text2)

    editorial = None
    date = None

    try:
        # Detect the editorial and use appropriate date format
        if "LA RAZON" in text or "LARAZON" in text or "LA RAZON" in text2 or "LARAZON" in text2:
            editorial = "LA RAZON"
            match = re.search(r'\b(?:lunes|martes|miércoles|jueves|viernes|sábado|domingo) (\d{1,2}) de (\w+) de (\d{4})\b', text, re.IGNORECASE)
            if match:
                day, month, year = match.groups()
                date = datetime.strptime(f"{day} {month} {year}", "%d %B %Y").strftime("%d/%m/%Y")
        
        elif "ABC" in text or "ABC" in text2:
            editorial = "ABC"
            match = re.search(r'\b(\d{1,2}) (\w+) (\d{4})\b', text, re.IGNORECASE)
            if match:
                day, month, year = match.groups()
                date = datetime.strptime(f"{day} {month} {year}", "%d %B %Y").strftime("%d/%m/%Y")
        
        elif "MUNDO" in text or "MUNDO" in text2:
            editorial = "EL MUNDO"
            match = re.search(r'\b(?:lunes|martes|miércoles|jueves|viernes|sábado|domingo) (\d{1,2}) de (\w+) de (\d{4})\b', text, re.IGNORECASE)
            if match:
                day, month, year = match.groups()
                date = datetime.strptime(f"{day} {month} {year}", "%d %B %Y").strftime("%d/%m/%Y")

    except ValueError:
        date = None

    return editorial, date
