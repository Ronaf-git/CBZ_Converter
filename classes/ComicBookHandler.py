import os
import tempfile
from functions.logging_config import setup_logger  
logger = setup_logger(__name__)

class ComicBookHandler:
    def __init__(self, input_file, output_folder=None):
        """Initialize with input comic file and optional output folder."""
        logger.info(f"Initializing ComicBookHandler with input_file={input_file}")
        self.input_file = input_file
        self.output_folder = output_folder if output_folder else os.path.dirname(input_file)
        
        # Create a temporary directory that will be cleaned up automatically
        self.temp_folder = tempfile.TemporaryDirectory()
        logger.info(f"Temporary directory created: {self.temp_folder.name}")

    def clean_up(self):
        """Ensure cleanup of temporary folder."""
        if self.temp_folder:
            logger.info(f"Cleaning up temporary directory: {self.temp_folder.name}")
            self.temp_folder.cleanup()

    def __str__(self):
        """Override string representation for user-friendly output."""
        return f"ComicBookHandler(input_file={self.input_file}, output_folder={self.output_folder})"

