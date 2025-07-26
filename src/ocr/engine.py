# File: src/ocr/engine.py

from paddleocr import PaddleOCR
import os

# Initialize the OCR engine once when the module is loaded.
OCR_ENGINE = PaddleOCR(use_angle_cls=True, lang='en')

def perform_ocr(image_path: str) -> list:
    """
    Performs OCR on a given image file.

    Args:
        image_path (str): The full path to the image file.

    Returns:
        list: A list of the raw detection results. Each item in the list
              is a list containing the bounding box coordinates and a tuple
              with the recognized text and its confidence score.
              Example: [[[x1,y1], [x2,y2], [x3,y3], [x4,y4]], ('text', 0.99)]
              Returns an empty list if no text is found or path is invalid.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image path does not exist: {image_path}")
        return []

    # Perform OCR on the image.
    result = OCR_ENGINE.ocr(image_path, cls=True)
    
    # Return the detailed result structure if it exists
    return result[0] if result and result[0] is not None else []