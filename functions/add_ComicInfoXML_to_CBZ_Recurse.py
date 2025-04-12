from functions.logging_config import logger  # Import the logger from logger_config
import os
from classes import *

def add_ComicInfoXML_to_CBZ_Recurse(root_folder) :
    """Recursively process all CBR, EPUB, and PDF files in a folder and convert them to CBZ."""
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
            
            if file.lower().endswith('.cbz'):
                logger.info(f"Updating ComicInfo.XML in {file_path}")
                cbz_handler = CBZHandler(file_path)
                cbz_handler.add_comic_info_to_cbz()