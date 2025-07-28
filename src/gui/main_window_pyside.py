# File: src/gui/main_window_pyside.py

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QTextEdit,
    QPushButton, QRadioButton, QComboBox, QHBoxLayout, QVBoxLayout, 
    QFrame, QFileDialog, QButtonGroup
)
from PySide6.QtCore import Qt, QRunnable, Slot, QThreadPool, QObject, Signal

# Import all our backend logic
from src.file_processor import process_file
from src.layout_parser.parser import parse_layout
from src.utils.exporter import export_to_pdf
from src.translator.engine import translate_text
from src.database.manager import setup_database, add_record

# --- Worker Thread for Translation ---
class WorkerSignals(QObject):
    finished = Signal(str)

class TranslatorWorker(QRunnable):
    def __init__(self, text, source_lang, target_lang):
        super().__init__()
        self.signals = WorkerSignals()
        self.text = text
        self.source_lang = source_lang
        self.target_lang = target_lang

    @Slot()
    def run(self):
        result = translate_text(self.text, self.source_lang, self.target_lang)
        self.signals.finished.emit(result)

# --- Main Application Window ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPU-Based OCR Tool (PySide6)")
        self.resize(1100, 800)
        
        setup_database()
        self.threadpool = QThreadPool()

        # ---- UI Layout (omitted for brevity, it's the same as before) ----
        main_layout = QHBoxLayout()
        left_panel_layout = QVBoxLayout()
        right_panel_layout = QVBoxLayout()
        left_panel_widget = QFrame()
        left_panel_widget.setFixedWidth(250)
        left_panel_widget.setLayout(left_panel_layout)
        self.select_file_btn = QPushButton("Select File")
        self.copy_text_btn = QPushButton("Copy Text")
        self.save_txt_btn = QPushButton("Save as .txt")
        self.save_pdf_btn = QPushButton("Save as .pdf")
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setStyleSheet("background-color: #D32F2F;")
        left_panel_layout.addWidget(self.select_file_btn)
        left_panel_layout.addWidget(self.copy_text_btn)
        left_panel_layout.addWidget(self.save_txt_btn)
        left_panel_layout.addWidget(self.save_pdf_btn)
        left_panel_layout.addWidget(self.clear_btn)
        parser_label = QLabel("Parser Mode:")
        self.general_radio = QRadioButton("General Text")
        self.document_radio = QRadioButton("Structured Document")
        self.general_radio.setChecked(True)
        self.parser_button_group = QButtonGroup()
        self.parser_button_group.addButton(self.general_radio, 1)
        self.parser_button_group.addButton(self.document_radio, 2)
        left_panel_layout.addSpacing(20)
        left_panel_layout.addWidget(parser_label)
        left_panel_layout.addWidget(self.general_radio)
        left_panel_layout.addWidget(self.document_radio)
        translation_label = QLabel("Source Language:")
        self.lang_combo = QComboBox()
        self.languages = ["English", "Spanish", "French", "German", "Chinese", "Japanese", "Korean", "Russian"]
        self.lang_combo.addItems(self.languages)
        self.translate_btn = QPushButton("Translate to English")
        left_panel_layout.addSpacing(20)
        left_panel_layout.addWidget(translation_label)
        left_panel_layout.addWidget(self.lang_combo)
        left_panel_layout.addStretch()
        left_panel_layout.addWidget(self.translate_btn)
        right_panel_widget = QWidget()
        right_panel_widget.setLayout(right_panel_layout)
        self.image_label = QLabel("Select a file to begin")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFrameShape(QFrame.Shape.StyledPanel)
        self.output_textbox = QTextEdit()
        self.translated_textbox = QTextEdit()
        right_panel_layout.addWidget(self.image_label, 1)
        right_panel_layout.addWidget(self.output_textbox, 1)
        right_panel_layout.addWidget(self.translated_textbox, 1)
        main_layout.addWidget(left_panel_widget)
        main_layout.addWidget(right_panel_widget)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # ---- Connect Signals ----
        self.select_file_btn.clicked.connect(self.select_file)
        self.clear_btn.clicked.connect(self.clear_ui)
        self.copy_text_btn.clicked.connect(self.copy_text)
        self.save_txt_btn.clicked.connect(self.save_as_txt)
        self.save_pdf_btn.clicked.connect(self.save_as_pdf)
        self.translate_btn.clicked.connect(self.on_translate_click)
        self.output_textbox.textChanged.connect(self.handle_text_change)

    # ---- Backend Methods ----
    def on_translate_click(self):
        self.original_text_for_db = self.output_textbox.toPlainText() # Save for later
        if not self.original_text_for_db.strip():
            return

        selected_lang_name = self.lang_combo.currentText()
        translator_map = {
            "English": "en", "Spanish": "es", "French": "fr", "German": "de", 
            "Chinese": "zh", "Japanese": "ja", "Korean": "ko", "Russian": "ru"
        }
        source_lang_code = translator_map.get(selected_lang_name)
        
        self.translated_textbox.setText(f"Translating from {selected_lang_name}...")
        
        # Run translation in a background thread
        worker = TranslatorWorker(self.original_text_for_db, source_lang_code, 'en')
        worker.signals.finished.connect(self.on_translation_finished)
        self.threadpool.start(worker)

    def on_translation_finished(self, translated_text):
        self.translated_textbox.setText(translated_text)
        if "Error:" not in translated_text:
            add_record(profile_name="default", original_text=self.original_text_for_db, translated_text=translated_text)

    def select_file(self):
        # ... select_file logic is the same ...
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File", "", "All Files (*);;Image Files (*.png *.jpg *.jpeg);;PDF Files (*.pdf)")
        if not file_path: return
        self.clear_ui()
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
        else: self.image_label.setText(f"File:\n{file_path.split('/')[-1]}")
        self.output_textbox.setText("Processing...")
        QApplication.processEvents()
        lang_code = self.lang_map.get(self.lang_combo.currentText(), 'latin')
        raw_data = process_file(file_path, lang_code=lang_code)
        mode = "document" if self.document_radio.isChecked() else "general"
        formatted_text = parse_layout(raw_data, mode=mode)
        self.output_textbox.setText(formatted_text)
        
    def handle_text_change(self):
        self.translated_textbox.clear() # Clear translation if original text changes
        
    # All other methods (save, copy, clear, etc.) are the same
    def _get_full_content_for_saving(self):
        original_text = self.output_textbox.toPlainText().strip()
        translated_text = self.translated_textbox.toPlainText().strip()
        if not original_text: return None
        if translated_text and "Translating from" not in translated_text:
            return f"--- ORIGINAL TEXT ---\n{original_text}\n\n--- TRANSLATED TEXT ---\n{translated_text}"
        else: return original_text

    def save_as_txt(self):
        content = self._get_full_content_for_saving()
        if not content: return
        file_path, _ = QFileDialog.getSaveFileName(self, "Save as Text", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f: f.write(content)

    def save_as_pdf(self):
        content = self._get_full_content_for_saving()
        if not content: return
        file_path, _ = QFileDialog.getSaveFileName(self, "Save as PDF", "", "PDF Files (*.pdf)")
        if file_path:
            try: export_to_pdf(content, file_path)
            except Exception as e: print(f"Error exporting to PDF: {e}")

    def copy_text(self):
        QApplication.clipboard().setText(self.output_textbox.toPlainText())

    def clear_ui(self):
        self.image_label.clear(); self.image_label.setText("Select a file to begin")
        self.output_textbox.clear(); self.translated_textbox.clear()