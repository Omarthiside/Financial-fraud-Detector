import cv2
import numpy as np
from pdf2image import convert_from_bytes
import sys

class DocumentPreprocessor:
    def preprocess(self, file_bytes):
        try:
            poppler_path = r"/opt/homebrew/bin" 
            
            pil_images = convert_from_bytes(file_bytes, dpi=300, poppler_path=poppler_path)
            processed_images = []

            for pil_img in pil_images:
                img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
                processed_images.append(thresh)
                
            return processed_images
        
        except Exception as e:
            print(f"❌ Preprocessing Error: {e}")
            return []