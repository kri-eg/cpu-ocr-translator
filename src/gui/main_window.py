# File: src/gui/main_window.py

import customtkinter as ctk
from customtkinter import filedialog
from PIL import Image

from src.ocr.engine import perform_ocr

class App(ctk.CTk):
    """
    The main application window class.
    """
    def __init__(self):
        super().__init__()

        self.title("CPU-Based OCR Tool")
        self.geometry("1100x700")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.left_frame = ctk.CTkFrame(master=self, width=200, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.right_frame = ctk.CTkFrame(master=self)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.right_frame.grid_rowconfigure(0, weight=5) # Give more weight to the image
        self.right_frame.grid_rowconfigure(1, weight=4) # Give less weight to the text
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.left_frame.grid_rowconfigure(0, minsize=10)
        
        self.select_image_button = ctk.CTkButton(
            master=self.left_frame,
            text="Select Image",
            command=self.select_image
        )
        self.select_image_button.grid(row=1, column=0, padx=20, pady=10)
        
        self.image_label = ctk.CTkLabel(master=self.right_frame, text="Select an image to begin")
        self.image_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.output_textbox = ctk.CTkTextbox(master=self.right_frame, font=("Arial", 14))
        self.output_textbox.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    def _resize_image(self, image, max_width, max_height):
        """
        Resizes a PIL image to fit within max_width and max_height while preserving aspect ratio.
        """
        original_width, original_height = image.size
        ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        return (new_width, new_height)

    def select_image(self):
        """
        Opens a file dialog, displays the selected image proportionally, and performs OCR.
        """
        image_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )

        if image_path:
            # First, update the GUI to get the real size of the image_label widget
            self.update_idletasks() 
            
            # 1. Display the image proportionally
            image = Image.open(image_path)
            
            # Calculate the new proportional size using our helper method
            new_size = self._resize_image(
                image, 
                self.image_label.winfo_width(), 
                self.image_label.winfo_height()
            )

            ctk_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=new_size
            )
            self.image_label.configure(image=ctk_image, text="")

            # 2. Perform OCR on the selected image
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("0.0", "Processing...")
            self.update_idletasks()
            
            extracted_text = perform_ocr(image_path)
            
            # 3. Display the extracted text
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("0.0", extracted_text)