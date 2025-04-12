import os
import zipfile
import fitz  # PyMuPDF
from .ComicBookHandler import *
import subprocess
import re

class PDFHandler(ComicBookHandler):
    def __init__(self, input_file):
        # Check if the input file exists and is a valid PDF file
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"The input file {input_file} does not exist.")
        
        if not input_file.lower().endswith('.pdf'):
            raise ValueError(f"The file {input_file} is not a valid PDF file.")
        
        # Call parent constructor
        super().__init__(input_file)

    def update_pdf_metadata(self):
        input_file = self.input_file
        # Step 1: Get the folder where the PDF is located
        folder = os.path.basename(os.path.dirname(input_file))
        
        # Step 2: Extract the first numerical value from the PDF filename
        filename = os.path.basename(input_file)
        series_index = re.search(r'\d+', filename)
        
        if series_index:
            series_index = series_index.group(0)  # Get the first numerical value
        else:
            logger.info(f"No numerical value found in the filename: {filename}")
            return
        
        # Step 3: Update metadata using Calibre's ebook-meta command
        command = [
            'ebook-meta', input_file,  # Command and the file path
            '--series', folder,
            '--index', series_index,  # Set the series index as the title (optional)
        ]
        try:
            # Execute the command
            subprocess.run(command, check=True)
            logger.info(f"Metadata updated successfully for: {filename}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error updating metadata for {filename}: {e}")

    def convert_to_cbz(self, output_cbz_path=None):
        """Convert PDF to CBZ."""
        # If output_cbz_path is not provided, generate it based on input_file's directory and name
        if not output_cbz_path:
            output_cbz_path = os.path.splitext(self.input_file)[0] + ".cbz"
        """Convert PDF to CBZ."""
        image_paths = []
        doc = fitz.open(self.input_file)
        for page_num in range(doc.page_count):
            image_path = self.render_page_as_image(page_num)
            image_paths.append(image_path)

        with zipfile.ZipFile(output_cbz_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for image_path in image_paths:
                zipf.write(image_path, os.path.basename(image_path))
                os.remove(image_path)  # Clean up the temporary images

        logger.info(f"Converted {self.input_file} to {output_cbz_path}")
        self.clean_up()

    def render_page_as_image(self, page_num):
        """Render a PDF page as an image and save it to the temporary folder."""
        doc = fitz.open(self.input_file)
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))  # Render at 1:1 scaling
        image_path = os.path.join(self.temp_folder.name, f"page_{page_num + 1}.jpg")
        pix.save(image_path)
        
        return image_path
