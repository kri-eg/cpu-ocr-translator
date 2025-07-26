# File: src/gui/main_window.py

import customtkinter as ctk
from customtkinter import filedialog
from PIL import Image

from src.file_processor import process_file
from src.layout_parser.parser import parse_layout
from src.utils.exporter import export_to_pdf # NEW: Import the PDF exporter

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CPU-Based OCR Tool")
        self.geometry("1100x700")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.left_frame = ctk.CTkFrame(master=self, width=250, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.right_frame = ctk.CTkFrame(master=self)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.right_frame.grid_rowconfigure(0, weight=5)
        self.right_frame.grid_rowconfigure(1, weight=4)
        self.right_frame.grid_columnconfigure(0, weight=1)

        # ---- Configure the left frame widgets ----
        self.left_frame.grid_rowconfigure(8, weight=1) # Add a spacer row

        self.select_file_button = ctk.CTkButton(master=self.left_frame, text="Select File", command=self.select_file)
        self.select_file_button.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.copy_button = ctk.CTkButton(master=self.left_frame, text="Copy Text", command=self.copy_text)
        self.copy_button.grid(row=1, column=0, padx=20, pady=10)

        # ---- NEW: Save Buttons ----
        self.save_txt_button = ctk.CTkButton(master=self.left_frame, text="Save as .txt", command=self.save_as_txt)
        self.save_txt_button.grid(row=2, column=0, padx=20, pady=10)
        
        self.save_pdf_button = ctk.CTkButton(master=self.left_frame, text="Save as .pdf", command=self.save_as_pdf)
        self.save_pdf_button.grid(row=3, column=0, padx=20, pady=10)

        self.clear_button = ctk.CTkButton(master=self.left_frame, text="Clear", command=self.clear_ui, fg_color="#D32F2F", hover_color="#B71C1C")
        self.clear_button.grid(row=4, column=0, padx=20, pady=10)
        
        self.parser_mode_label = ctk.CTkLabel(master=self.left_frame, text="Parser Mode:", font=ctk.CTkFont(weight="bold"))
        self.parser_mode_label.grid(row=5, column=0, padx=20, pady=(20, 0), sticky="w")

        self.parser_mode = ctk.StringVar(value="general")
        self.radio_general = ctk.CTkRadioButton(master=self.left_frame, text="General Text", variable=self.parser_mode, value="general")
        self.radio_general.grid(row=6, column=0, padx=20, pady=10, sticky="w")
        self.radio_document = ctk.CTkRadioButton(master=self.left_frame, text="Structured Document", variable=self.parser_mode, value="document")
        self.radio_document.grid(row=7, column=0, padx=20, pady=10, sticky="w")
        
        self.image_label = ctk.CTkLabel(master=self.right_frame, text="Select an Image or PDF to begin")
        self.image_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.output_textbox = ctk.CTkTextbox(master=self.right_frame, font=("Arial", 14))
        self.output_textbox.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.output_textbox.bind("<Control-a>", self._select_all)
        self.output_textbox.bind("<Control-A>", self._select_all)
    
    # ---- NEW: Methods for Saving Files ----
    def save_as_txt(self):
        text_content = self.output_textbox.get("1.0", "end-1c") # Get all text except the last newline
        if not text_content.strip():
            return # Do nothing if there is no text
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text_content)

    def save_as_pdf(self):
        text_content = self.output_textbox.get("1.0", "end-1c")
        if not text_content.strip():
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                export_to_pdf(text_content, file_path)
            except Exception as e:
                # Handle exceptions, like the font file not being found
                print(f"Error exporting to PDF: {e}")
                # You could show an error message to the user here
                error_dialog = ctk.CTkInputDialog(text=f"Error exporting to PDF:\n{e}", title="Error")
    
    # ---- Other methods ----
    def copy_text(self):
        # ... (rest of the file is unchanged)
        text = self.output_textbox.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(text)
        self.copy_button.configure(text="Copied!")
        self.after(2000, lambda: self.copy_button.configure(text="Copy Text"))

    def clear_ui(self):
        self.image_label.configure(image=None, text="Select an Image or PDF to begin")
        self.output_textbox.delete("1.0", "end")

    def _select_all(self, event=None):
        self.output_textbox.tag_add("sel", "1.0", "end")
        return "break"

    def _resize_image(self, image, max_width, max_height):
        original_width, original_height = image.size
        ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        return (new_width, new_height)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image or PDF",
            filetypes=[("All Files", "*.png *.jpg *.jpeg *.bmp *.pdf"), ("PDF Files", "*.pdf"), ("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if not file_path: return

        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            self.update_idletasks() 
            image = Image.open(file_path)
            new_size = self._resize_image(image, self.image_label.winfo_width(), self.image_label.winfo_height())
            ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=new_size)
            self.image_label.configure(image=ctk_image, text="")
        else:
            self.image_label.configure(image=None, text=f"File:\n{file_path.split('/')[-1]}", font=("Arial", 16))

        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("0.0", "Processing...")
        self.update_idletasks()
        
        raw_data = process_file(file_path)
        selected_mode = self.parser_mode.get()
        formatted_text = parse_layout(raw_data, mode=selected_mode)
        
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("0.0", formatted_text)