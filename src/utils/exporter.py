# File: src/utils/exporter.py

from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        pass # No header needed
    def footer(self):
        pass # No footer needed

def export_to_pdf(text: str, file_path: str):
    """
    Exports a string of text to a PDF file.

    Args:
        text (str): The text content to export.
        file_path (str): The path to save the PDF file.
    """
    pdf = PDF()
    pdf.add_page()

    # Add the DejaVu font for better Unicode character support.
    # Ensure the .ttf file is in the specified path.
    font_path = os.path.join("src", "assets", "fonts", "DejaVuSans.ttf")
    if not os.path.exists(font_path):
        raise FileNotFoundError("Font file not found: DejaVuSans.ttf. Please download it and place it in the assets/fonts directory.")

    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    # Use multi_cell to handle line breaks and automatic page breaks.
    pdf.multi_cell(0, 5, text)

    pdf.output(file_path)