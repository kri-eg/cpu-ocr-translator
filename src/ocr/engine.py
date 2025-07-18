# File: src/ocr/engine.py

from paddleocr import PaddleOCR
import os

# Initialize the OCR engine once when the module is loaded.
# This is more efficient than re-initializing it every time.
# We specify CPU use and English language support.
OCR_ENGINE = PaddleOCR(use_angle_cls=True, lang='en')

def perform_ocr(image_path: str) -> str:
    """
    Performs OCR on a given image file and returns the extracted text as a single string.

    Args:
        image_path (str): The full path to the image file.

    Returns:
        str: The extracted text, with each line separated by a newline character.
             Returns an error message if the path is invalid.
    """
    if not os.path.exists(image_path):
        return "Error: Image path does not exist."

    # Perform OCR on the image.
    result = OCR_ENGINE.ocr(image_path, cls=True)

    extracted_lines = []
    if result and result[0] is not None:
        for line_data in result[0]:
            # The text is the first element of the second item in the line_data tuple
            text = line_data[1][0]
            extracted_lines.append(text)

    # Join all the detected lines into a single string with newlines
    return "\n".join(extracted_lines)