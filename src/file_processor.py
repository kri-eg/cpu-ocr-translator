# File: src/file_processor.py

import fitz  # PyMuPDF
from src.ocr.engine import perform_ocr
import io
from PIL import Image

def process_file(file_path: str) -> list:
    """
    Processes a file (image or PDF) and returns structured OCR data.

    Args:
        file_path (str): The path to the file.

    Returns:
        list: A list of text blocks with coordinates, compatible with the layout parser.
    """
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        # It's an image, use the existing OCR engine
        return perform_ocr(file_path)
    elif file_path.lower().endswith('.pdf'):
        # It's a PDF, process it
        return _process_pdf(file_path)
    else:
        print(f"Unsupported file type: {file_path}")
        return []

def _process_pdf(file_path: str) -> list:
    """
    Handles PDF processing. Tries direct text extraction first, falls back to OCR.
    """
    doc = fitz.open(file_path)
    
    # For simplicity, we'll process only the first page.
    if len(doc) == 0:
        return []
    
    page = doc[0]
    
    # --- Strategy 1: Try to extract text directly ---
    text = page.get_text().strip()
    
    # If we get a good amount of text, assume it's a text-based PDF.
    if len(text) > 100: # Heuristic: more than 100 characters means it's likely text-based
        # We need to return data in the same format as PaddleOCR.
        # We'll create dummy bounding boxes for each line.
        blocks = page.get_text("blocks")
        ocr_like_results = []
        for b in blocks:
            # b format: (x0, y0, x1, y1, "text", block_no, block_type)
            box = [[b[0], b[1]], [b[2], b[1]], [b[2], b[3]], [b[0], b[3]]]
            text_tuple = (b[4].strip(), 0.99) # text and dummy confidence
            if text_tuple[0]: # Only add if there's text
                 ocr_like_results.append([box, text_tuple])
        return ocr_like_results

    # --- Strategy 2: Fallback to OCR for image-based PDFs ---
    # Convert the page to an image
    pix = page.get_pixmap(dpi=200) # Higher DPI for better OCR quality
    img_bytes = pix.tobytes("png")
    
    # Save the bytes to a temporary in-memory file for PaddleOCR
    temp_image_path = io.BytesIO(img_bytes)
    
    # Run OCR on the converted image
    return perform_ocr(temp_image_path)