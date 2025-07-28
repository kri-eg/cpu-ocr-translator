# File: src/ocr/engine.py

from paddleocr import PaddleOCR
import os

# Initialize multiple OCR engines for different languages
OCR_ENGINES = {
    'en': PaddleOCR(use_angle_cls=True, lang='en'),
    'ch': PaddleOCR(use_angle_cls=True, lang='ch'),
    'korean': PaddleOCR(use_angle_cls=True, lang='korean'),
    'japan': PaddleOCR(use_angle_cls=True, lang='japan'),
    'latin': PaddleOCR(use_angle_cls=True, lang='latin'),
    'cyrillic': PaddleOCR(use_angle_cls=True, lang='cyrillic'),
}

def perform_ocr(image_path: str, language: str = 'latin') -> list:
    """
    Performs OCR on a given image file with language support.
    
    Args:
        image_path (str): The full path to the image file.
        language (str): Language code ('en', 'ch', 'korean', 'japan', 'latin', 'cyrillic')
        
    Returns:
        list: A list of the raw detection results.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image path does not exist: {image_path}")
        return []
    
    # Select appropriate OCR engine, default to latin
    engine = OCR_ENGINES.get(language, OCR_ENGINES['latin'])
    
    result = engine.ocr(image_path, cls=True)
    return result[0] if result and result[0] is not None else []