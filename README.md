CPU-Based Multilingual OCR & Translation Tool
Introduction

This document provides a comprehensive overview of the CPU-Based Multilingual OCR & Translation Tool, a standalone desktop application built with Python. The primary function of this application is to extract text from image and PDF files, intelligently format the extracted content based on its layout, and provide offline translation of the text into English. The project prioritizes stability, accuracy, and offline functionality, operating entirely on a CPU architecture.
Features

    Multilingual OCR: Utilizes specialized PaddleOCR models to accurately extract text from a wide range of languages, including English, Spanish, French, German, Russian, Chinese, Japanese, and Korean.

    Multi-Format Input: Supports processing for common image formats (.png, .jpg, .jpeg) as well as both text-based and image-based (scanned) .pdf files.

    Intelligent Layout Parser: Goes beyond raw text extraction by offering two user-selectable parsing modes for optimized output formatting:

        General Text: A robust parser designed for unstructured, scattered, or rotated text.

        Structured Document: An advanced parser that reconstructs multi-column layouts and paragraph spacing, ideal for clean documents like articles or resumes.

    Fully Offline Translation: Translates extracted text into English using the Argos Translate library. Required language models are downloaded automatically on first use and subsequently work completely offline, ensuring user privacy.

    History Database: Automatically saves all OCR and translation results to a local SQLite database, creating a persistent record of all processed files.

    History Viewer: A separate, scrollable window allows users to browse, view, and read all past records, turning the tool into a personal archive.

    Export Functionality: Enables users to save the final output (both original and translated text) to .txt and .pdf file formats.

    Graphical User Interface: A clean and intuitive desktop UI built with the CustomTkinter library.

Technology Stack

The technology stack was carefully selected to ensure stability, offline capability, and high performance on a standard CPU.

Component
	

Technology
	

Rationale

OCR Engine
	

PaddleOCR
	

Chosen for its high accuracy and excellent support for a wide range of languages.

Translation
	

Argos Translate
	

A powerful, open-source, and fully offline translation library.

GUI
	

CustomTkinter
	

Provides a good balance of modern aesthetics and simplicity for rapid UI development.

Database
	

SQLite
	

A serverless, file-based database natively supported by Python; ideal for local data storage.

PDF Handling
	

PyMuPDF, fpdf2
	

Used for high-performance PDF reading and simple PDF generation for export.
System Requirements & Setup

To set up and run this project, your system must meet the following prerequisites.
Prerequisites

    Python version 3.10

    git for cloning the repository

    Access to an internet connection for the initial download of dependencies and translation models.

Installation Steps

    Clone the Repository:
    Open a terminal and clone the project repository to your local machine.

    git clone https://github.com/your-username/cpu-ocr-translator.git
    cd cpu-ocr-translator

    Create and Activate a Python 3.10 Virtual Environment:
    It is highly recommended to use a virtual environment to manage project dependencies.

    # Create the environment
    python3.10 -m venv venv

    # Activate it on Linux/macOS
    source venv/bin/activate

    # Activate it on Windows
    venv\Scripts\activate

    Install Dependencies:
    All required Python packages are listed in the requirements.txt file. Install them using pip.

    pip install -r requirements.txt

    Download Font for PDF Export:
    The PDF export feature requires a font file that supports a wide range of Unicode characters.

        Create the necessary directory structure: src/assets/fonts/.

        Download the DejaVuSans.ttf font file from the official DejaVu Fonts website.

        Place the DejaVuSans.ttf file inside the src/assets/fonts/ directory.

    Run the Application:
    Once the setup is complete, you can launch the application by running the main script from the project's root directory.

    python main.py

    Note: The application may start slowly the first time as it initializes the OCR models into memory. Similarly, the first translation for a new language will be slow as it downloads the required model.

User Guide

    Select Source Language: From the dropdown menu on the left, choose the primary language of the document you intend to process. This will select the most accurate OCR engine for the task.

    Select Parser Mode:

        Choose "General Text" for most images, especially those with rotated or scattered text.

        Choose "Structured Document" for clean, multi-column documents like resumes or articles to achieve better formatting.

    Select File: Click the "Select File" button to open a file dialog and choose a supported image or PDF file.

    Translate (Optional): After the text has been extracted, click the "Translate to English" button to generate the English translation.

    View History: Click the "View History" button to open a new window displaying a scrollable list of all your past results.

    Save/Export: Use the "Save as .txt" or "Save as .pdf" buttons to export the original and translated text to a file.