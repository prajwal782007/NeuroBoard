import pytesseract
import base64
import numpy as np
import cv2

class MathRecognizer:
    def extract_text(self, image_base64: str) -> str:
        """
        Decodes a base64 image and uses OpenCV and pytesseract 
        to extract the mathematical equation.
        """
        # Decode base64 
        encoded_data = image_base64.split(',', 1)[-1] if ',' in image_base64 else image_base64
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        
        # Preprocessing to improve OCR accuracy
        # Inverse thresholding so text is white on black background, if needed.
        # But simple thresholding often helps OCR:
        _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        # OCR config focused on math characters and single lines
        # textord_equation_detect triggers tesseract's equation detector
        custom_config = r'--psm 7 -c tessedit_char_whitelist=0123456789+-*/=xyXY().'
        text = pytesseract.image_to_string(thresh, config=custom_config)
        
        return text.strip()
