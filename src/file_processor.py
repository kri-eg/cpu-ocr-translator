# File: src/file_processor.py

import fitz  # PyMuPDF
from src.ocr.engine import perform_ocr
import io

def process_file(file_path: str, lang_code: str) -> list: # UPDATED: Accepts lang_code
    """
    Processes a file (image or PDF) and returns structured OCR data.
    """
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        # UPDATED: Pass the lang_code to the OCR engine
        return perform_ocr(file_path, language=lang_code)
    elif file_path.lower().endswith('.pdf'):
        # UPDATED: Pass the lang_code to the PDF processor
        return _process_pdf(file_path, lang_code=lang_code)
    else:
        print(f"Unsupported file type: {file_path}")
        return []

def _process_pdf(file_path: str, lang_code: str) -> list: # UPDATED: Accepts lang_code
    """
    Handles PDF processing. Tries direct text extraction first, falls back to OCR.
    """
    doc = fitz.open(file_path)
    if len(doc) == 0:
        return []
    
    page = doc[0]
    text = page.get_text().strip()
    
    if len(text) > 100:
        blocks = page.get_text("blocks")
        ocr_like_results = []
        for b in blocks:
            box = [[b[0], b[1]], [b[2], b[1]], [b[2], b[3]], [b[0], b[3]]]
            text_tuple = (b[4].strip(), 0.99)
            if text_tuple[0]:
                 ocr_like_results.append([box, text_tuple])
        return ocr_like_results

    pix = page.get_pixmap(dpi=200)
    img_bytes = pix.tobytes("png")
    temp_image_path = io.BytesIO(img_bytes)
    
    # UPDATED: Pass the lang_code when falling back to OCR
    return perform_ocr(temp_image_path, language=lang_code)