import os
import zipfile
from .ComicBookHandler import *

class EPUBHandler(ComicBookHandler):
    def __init__(self, input_file, temp_folder):
        # Check if the input file exists and is a valid EPUB file
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"The input file {input_file} does not exist.")
        
        if not input_file.lower().endswith('.epub'):
            raise ValueError(f"The file {input_file} is not a valid EPUB file.")
        
        super().__init__(input_file)
        self.temp_folder = temp_folder
        
    def convert_to_cbz(self, output_cbz_path=None):
        """Convert PDF to CBZ."""
        # If output_cbz_path is not provided, generate it based on input_file's directory and name
        if not output_cbz_path:
            output_cbz_path = os.path.splitext(self.input_file)[0] + ".cbz"
        """Convert EPUB to CBZ."""
        with zipfile.ZipFile(self.input_file) as epub:
            with zipfile.ZipFile(output_cbz_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in epub.namelist():
                    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        epub.extract(file, self.temp_folder.name)
                        zipf.write(os.path.join(self.temp_folder.name, file), file)
        logger.info(f"Converted {self.input_file} to {output_cbz_path}")
        self.clean_up()