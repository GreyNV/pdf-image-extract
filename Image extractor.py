from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
import io
import re
import cv2
import numpy as np

file_path = 'C:/Users/AndriiRybak/Rhodium/Merging project/Merged_AL-Birmingham.pdf'
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\AndriiRybak\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

reader = PdfReader(file_path)

for i in range(len(reader.pages)):
    page = reader.pages[i]
    print(f"Page {i+1}:")
    for image_file_object in page.images:
        image_data = image_file_object.data
        image_bytes = io.BytesIO(image_data)
        image = Image.open(image_bytes)
        image_bytes_raw = image_bytes.getvalue()
        image_np = np.frombuffer(image_bytes_raw, np.uint8)
        image_decoded = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        
        gray = cv2.cvtColor(image_decoded, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('gray', gray)
        thresh = cv2.threshold(gray,100 ,100, cv2.THRESH_BINARY_INV)[1]
        thresh = 255 - thresh

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        result = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        # cv2.imshow('thresh', thresh)
        # cv2.imshow('result', result)
        # cv2.imwrite('result.jpg', result)
        # invert = cv2.bitwise_not(result)
        image_text = pytesseract.pytesseract.image_to_string(result, lang='eng', output_type=pytesseract.Output.DICT, config='--psm 1')
        # print(image_text)
        if "Pipeline" in image_text['text']:
            cropped_image = result[105:721, 950:1588] # Slicing to crop the image
            print(result.shape)
            
            # cv2.imshow('image', cropped_image)
            # cv2.waitKey(0)

            image_text = pytesseract.pytesseract.image_to_string(cropped_image, lang='eng', output_type=pytesseract.Output.DICT, config='--psm 4 -c tessedit_char_whitelist=0123456789')
            extracted_text = image_text['text']
            # pipeline_text = image_text['text'].split("5", 1)[1]
            print(f"Extracted text: {extracted_text}")  # Print the extracted text (pipeline_text)
            # Find all numbers in the extracted text
            numbers = re.findall(r'\d+', extracted_text)
            print(f"Found numbers: {numbers}")  # Print the found numbers (numbers)
            # Convert found numbers to integers and sum them up
            total = sum(map(int, numbers))
            print(f"Total: {total}") # Print the total