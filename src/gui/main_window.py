# File: src/gui/main_window.py

import customtkinter as ctk
from customtkinter import filedialog
from PIL import Image

from src.file_processor import process_file
from src.layout_parser.parser import parse_layout
from src.utils.exporter import export_to_pdf
from src.translator.engine import translate_text

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CPU-Based OCR Tool")
        self.geometry("1100x800")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.left_frame = ctk.CTkFrame(master=self, width=250, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.right_frame = ctk.CTkFrame(master=self)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.right_frame.grid_rowconfigure(0, weight=1) 
        self.right_frame.grid_rowconfigure(1, weight=1) 
        self.right_frame.grid_rowconfigure(2, weight=1) 
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.left_frame.grid_rowconfigure(10, weight=1) 

        self.select_file_button = ctk.CTkButton(master=self.left_frame, text="Select File", command=self.select_file)
        self.select_file_button.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.copy_button = ctk.CTkButton(master=self.left_frame, text="Copy Text", command=self.copy_text)
        self.copy_button.grid(row=1, column=0, padx=20, pady=10)
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
        
        self.translation_label = ctk.CTkLabel(master=self.left_frame, text="Translate To English From:", font=ctk.CTkFont(weight="bold"))
        self.translation_label.grid(row=8, column=0, padx=20, pady=(20, 0), sticky="w")
        
        languages = ["Spanish", "French", "German", "Chinese", "Russian", "Japanese", "Korean"]
        self.lang_map = {"Spanish": "es", "French": "fr", "German": "de", "Chinese": "ch", "Russian": "ru", "Japanese": "ja", "Korean": "ko"}
        self.source_lang_menu = ctk.CTkOptionMenu(master=self.left_frame, values=languages)
        self.source_lang_menu.grid(row=9, column=0, padx=20, pady=10)
        self.translate_button = ctk.CTkButton(master=self.left_frame, text="Translate", command=self.on_translate_click)
        self.translate_button.grid(row=10, column=0, padx=20, pady=10, sticky="s")
        
        self.image_label = ctk.CTkLabel(master=self.right_frame, text="Select a file to begin")
        self.image_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.output_textbox = ctk.CTkTextbox(master=self.right_frame, font=("Arial", 14), wrap="word")
        self.output_textbox.grid(row=1, column=0, sticky="nsew", padx=5, pady=(5,0))
        self.translated_textbox = ctk.CTkTextbox(master=self.right_frame, font=("Arial", 14), wrap="word")
        self.translated_textbox.grid(row=2, column=0, sticky="nsew", padx=5, pady=(5,5))
        
        self.output_textbox.bind("<Control-a>", self._select_all_original)
        self.translated_textbox.bind("<Control-a>", self._select_all_translated)
        
    def on_translate_click(self):
        original_text = self.output_textbox.get("1.0", "end-1c")
        if not original_text.strip(): return
        selected_lang_name = self.source_lang_menu.get()
        source_lang_code = self.lang_map.get(selected_lang_name)
        
        # This map is for the translator, which uses different codes than PaddleOCR
        translator_lang_map = {"latin": "es", "en": "en", "ch": "zh", "japan": "ja", "korean": "ko", "cyrillic": "ru"}
        # We need to map the OCR language code to the 2-letter translator code
        ocr_code_to_translator_code = {
            "latin": "es", # Default Latin to Spanish for translation
            "en": "en",
            "ch": "zh",
            "japan": "ja",
            "korean": "ko",
            "cyrillic": "ru"
        }
        source_lang_code = ocr_code_to_translator_code.get(source_lang_code, "es")


        self.translated_textbox.delete("1.0", "end")
        self.translated_textbox.insert("0.0", f"Translating from {selected_lang_name}...")
        self.update_idletasks()
        
        translated_text = translate_text(original_text, source_lang=source_lang_code, target_lang='en')
        
        self.translated_textbox.delete("1.0", "end")
        self.translated_textbox.insert("0.0", translated_text)
        
    def _get_full_content_for_saving(self):
        """Helper function to get formatted text from both boxes."""
        original_text = self.output_textbox.get("1.0", "end-1c").strip()
        translated_text = self.translated_textbox.get("1.0", "end-1c").strip()

        if not original_text:
            return None

        # If there is translated text, combine both with headers
        if translated_text and "Translating from" not in translated_text:
            return (
                "--- ORIGINAL TEXT ---\n"
                f"{original_text}\n\n"
                "--- TRANSLATED TEXT ---\n"
                f"{translated_text}"
            )
        # Otherwise, just return the original text
        else:
            return original_text

    def save_as_txt(self):
        full_content = self._get_full_content_for_saving()
        if not full_content:
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(full_content)

    def save_as_pdf(self):
        full_content = self._get_full_content_for_saving()
        if not full_content:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                export_to_pdf(full_content, file_path)
            except Exception as e:
                print(f"Error exporting to PDF: {e}")
    
    def copy_text(self):
        text = self.output_textbox.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(text)
        self.copy_button.configure(text="Copied!")
        self.after(2000, lambda: self.copy_button.configure(text="Copy Text"))

    def clear_ui(self):
        if hasattr(self, 'image_label') and self.image_label.winfo_exists():
            self.image_label.destroy()
        self.image_label = ctk.CTkLabel(master=self.right_frame, text="Select a file to begin")
        self.image_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.output_textbox.delete("1.0", "end")
        self.translated_textbox.delete("1.0", "end")

    def _select_all_original(self, event=None):
        self.output_textbox.tag_add("sel", "1.0", "end")
        return "break"
        
    def _select_all_translated(self, event=None):
        self.translated_textbox.tag_add("sel", "1.0", "end")
        return "break"

    def _resize_image(self, image, max_width, max_height):
        original_width, original_height = image.size
        ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        return (new_width, new_height)

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("All Files", "*.*"), ("PDF Files", "*.pdf"), ("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if not file_path: return
        
        self.clear_ui()

        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            if hasattr(self, 'image_label') and self.image_label.winfo_exists():
                self.image_label.destroy()
            self.image_label = ctk.CTkLabel(master=self.right_frame, text="")
            self.image_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            self.update_idletasks()
            
            image = Image.open(file_path)
            new_size = self._resize_image(image, self.image_label.winfo_width(), self.image_label.winfo_height())
            ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=new_size)
            
            self.image_label.image = ctk_image
            self.image_label.configure(image=ctk_image, text="")
        else:
            self.image_label.configure(image=None, text=f"File:\n{file_path.split('/')[-1]}", font=("Arial", 16))

        self.output_textbox.insert("0.0", "Processing...")
        self.update_idletasks()
        
        selected_lang_name = self.source_lang_menu.get()
        lang_code = self.lang_map.get(selected_lang_name, 'latin')
        
        raw_data = process_file(file_path, lang_code=lang_code)
        
        selected_mode = self.parser_mode.get()
        formatted_text = parse_layout(raw_data, mode=selected_mode)
        
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("0.0", formatted_text)