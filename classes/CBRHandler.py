import os
import zipfile
import rarfile
rarfile.UNRAR_TOOL = r'C:\Program Files\WinRAR\unrar.exe'  

from .ComicBookHandler import *  

class CBRHandler(ComicBookHandler):
    def __init__(self, input_file, temp_folder=None):
        """Initialize the CBR handler with validation."""
        self.input_file = input_file
        self.temp_folder = temp_folder if temp_folder else 'temp_images'

        # Validate the CBR file during initialization     
        if not self.is_valid_cbr() and not self.is_valid_cbz():
            logger.error(f"{self.input_file} is not a valid CBR or CBZ file.")
            raise ValueError(f"{self.input_file} is not a valid CBR or CBZ file.")

        logger.info(f"Initialized CBRHandler for {self.input_file}")

    def is_valid_cbr(self):
        """Check if the file is a valid CBR archive."""
        if not self.input_file.lower().endswith('.cbr'):
            logger.warning(f"File {self.input_file} does not have a .cbr extension.")
            return False

        try:
            with rarfile.RarFile(self.input_file) as r:
                # If we can open it without errors, it's a valid CBR file
                logger.debug(f"Successfully opened {self.input_file} as a RAR archive.")
                return True
        except rarfile.Error:
            # If an error occurs, it's not a valid RAR file
            logger.error(f"Failed to open {self.input_file} as a valid RAR archive.")
            return False

    def is_valid_cbz(self):
        """Check if the file is a ZIP archive."""
        try:
            with zipfile.ZipFile(self.input_file, 'r') as zf:
                # If we can open it without errors, it's a valid CBZ file
                logger.debug(f"Successfully opened {self.input_file} as a ZIP archive.")
                return True
        except zipfile.BadZipFile:
            # If an error occurs, it's not a valid ZIP file
            logger.error(f"Failed to open {self.input_file} as a valid ZIP archive.")
            return False

    def convert_to_cbz(self, output_cbz_path=None):
        """Convert CBR to CBZ."""
        # If the file is already a valid CBZ, just rename the extension
        if self.is_valid_cbz():
            new_cbz_path = os.path.splitext(self.input_file)[0] + ".cbz"
            if new_cbz_path != self.input_file:
                os.rename(self.input_file, new_cbz_path)
                logger.info(f"{self.input_file} is already a valid CBZ. Renamed to {new_cbz_path}.")
            return  # No need to convert, it's already CBZ

        # If output_cbz_path is not provided, generate it based on input_file's directory and name
        if not output_cbz_path:
            output_cbz_path = os.path.splitext(self.input_file)[0] + ".cbz"

        logger.info(f"Converting {self.input_file} to {output_cbz_path}...")

        try:
            with rarfile.RarFile(self.input_file) as r:
                with zipfile.ZipFile(output_cbz_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file in r.infolist():
                        r.extract(file, self.temp_folder)
                        zipf.write(os.path.join(self.temp_folder, file.filename), file.filename)

            logger.info(f"Successfully converted {self.input_file} to {output_cbz_path}.")
        except Exception as e:
            logger.error(f"Error converting CBR to CBZ: {e}")
        finally:
            self.clean_up()