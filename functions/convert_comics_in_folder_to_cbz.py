import os
from classes import *
from functions.logging_config import logger  # Import the logger from logger_config

# Single function to process CBR, EPUB, and PDF files in a folder
def convert_comics_in_folder_to_cbz(root_folder):
    """Recursively process all CBR, EPUB, and PDF files in a folder and convert them to CBZ."""
    for root, dirs, files in os.walk(root_folder):
        for file in files: 
            file_path = os.path.join(root, file)
           
            if file.lower().endswith('.cbr'):
                cbr_handler = CBRHandler(file_path)
                cbr_handler.convert_to_cbz()

            elif file.lower().endswith('.epub'):
                epub_handler = EPUBHandler(file_path)
                epub_handler.convert_to_cbz()

            elif file.lower().endswith('.pdf'):
                pdf_handler = PDFHandler(file_path)
                pdf_handler.convert_to_cbz()