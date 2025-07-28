# File: src/gui/history_window.py

import customtkinter as ctk
from src.database.manager import get_all_records

class HistoryWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("History")
        self.geometry("800x600")

        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Saved Records")
        self.scrollable_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.display_records()

    def display_records(self):
        records = get_all_records()

        if not records:
            label = ctk.CTkLabel(self.scrollable_frame, text="No history found.")
            label.pack(pady=10, padx=10)
            return

        for record in records:
            timestamp, _, original_text, translated_text = record
            
            entry_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="gray20")
            entry_frame.pack(fill="x", padx=10, pady=5)
            
            timestamp_label = ctk.CTkLabel(entry_frame, text=f"Saved on: {timestamp}", font=ctk.CTkFont(weight="bold"))
            timestamp_label.pack(anchor="w", padx=10, pady=(5, 0))

            original_label = ctk.CTkLabel(entry_frame, text="Original:", font=ctk.CTkFont(slant="italic"))
            original_label.pack(anchor="w", padx=10, pady=(5, 0))
            original_text_box = ctk.CTkTextbox(entry_frame, height=80, wrap="word")
            original_text_box.insert("1.0", original_text)
            original_text_box.configure(state="disabled")
            original_text_box.pack(fill="x", expand=True, padx=10, pady=5)

            translated_label = ctk.CTkLabel(entry_frame, text="Translation:", font=ctk.CTkFont(slant="italic"))
            translated_label.pack(anchor="w", padx=10, pady=(5, 0))
            translated_text_box = ctk.CTkTextbox(entry_frame, height=80, wrap="word")
            translated_text_box.insert("1.0", translated_text)
            translated_text_box.configure(state="disabled")
            translated_text_box.pack(fill="x", expand=True, padx=10, pady=5)