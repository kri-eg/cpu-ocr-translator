# File: src/translator/engine.py

import argostranslate.package
import argostranslate.translate
import os
import threading

# Use a lock to prevent race conditions during the one-time model download
package_lock = threading.Lock()

def _get_translation(from_code, to_code):
    """Checks for installed language models and downloads them if necessary."""
    with package_lock:
        available_packages = argostranslate.package.get_installed_packages()

        # Check if the required translation package is already installed
        found_translation = any(
            p for p in available_packages 
            if p.from_code == from_code and p.to_code == to_code
        )

        if not found_translation:
            print(f"Downloading translation model: {from_code} -> {to_code}...")
            argostranslate.package.update_package_index()
            available_to_install = argostranslate.package.get_available_packages()
            package_to_install = next(
                filter(
                    lambda x: x.from_code == from_code and x.to_code == to_code,
                    available_to_install
                )
            )
            package_to_install.install()
            print("Download complete.")

    return argostranslate.translate.get_translation_from_codes(from_code, to_code)


def translate_text(text_to_translate: str, source_lang: str, target_lang: str) -> str:
    """
    Translates a block of text from a source language to a target language.

    Args:
        text_to_translate (str): The text to be translated.
        source_lang (str): The source language code (e.g., 'es' for Spanish).
        target_lang (str): The target language code (e.g., 'en' for English).

    Returns:
        str: The translated text.
    """
    try:
        translation = _get_translation(source_lang, target_lang)
        return translation.translate(text_to_translate)
    except Exception as e:
        print(f"Error during translation: {e}")
        return f"Error: Could not translate from '{source_lang}' to '{target_lang}'. Model may not be available."