# File: src/database/manager.py

import sqlite3
from datetime import datetime

DB_PATH = "history.db"

def setup_database():
    """Creates the database and the history table if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY,
        timestamp TEXT NOT NULL,
        profile_name TEXT NOT NULL,
        original_text TEXT,
        translated_text TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_record(profile_name: str, original_text: str, translated_text: str = "") -> int:
    """Adds a new record and returns the new record's ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO history (timestamp, profile_name, original_text, translated_text) VALUES (?, ?, ?, ?)",
        (timestamp, profile_name, original_text, translated_text)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def update_record_translation(record_id: int, translated_text: str):
    """Updates the translated_text for a specific record."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE history SET translated_text = ? WHERE id = ?",
        (translated_text, record_id)
    )
    conn.commit()
    conn.close()

def get_all_records() -> list:
    """Retrieves all records from the history table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, profile_name, original_text, translated_text FROM history ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()
    return records