import cv2
import pytesseract
import numpy as np
import matplotlib.pyplot as plt

# Function to preprocess a cropped image for OCR with additional sharpening and contrast
def preprocess_and_upscale(image_path, output_path, scale_factor=2.0):
    img = cv2.imread(image_path)
    
    # Convert to grayscale
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
    
    # Save the processed image
    cv2.imwrite(output_path, binary_img)
    
    return binary_img

# Function to perform OCR on the processed image
def ocr_on_cropped_image(image_path):
    output_path = "processed_cropped_image.png"
    
    # Preprocess the image by upscaling, enhancing contrast, and sharpening
    processed_img = preprocess_and_upscale(image_path, output_path)
    
    # Perform OCR on the processed image with configuration to recognize uppercase letters and numbers
    custom_config = "--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    extracted_text = pytesseract.image_to_string(processed_img, config=custom_config)
    
    # Print extracted text first
    print(f"Extracted text:\n{extracted_text}\n")
    
    # Display the processed image
    plt.imshow(processed_img, cmap='gray')
    plt.title('Upscaled, Sharpened, and Binarized Image for OCR')
    plt.axis('off')
    plt.show()
    
    return extracted_text

# Path to the cropped image containing "El Mundo" or the date
image_path = "larazon.png"  # Update this to the path of your image
ocr_on_cropped_image(image_path)