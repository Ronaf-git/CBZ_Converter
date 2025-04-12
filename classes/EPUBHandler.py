import os
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
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

    def rename_to_cbz(self):
        """
        Renames the input EPUB file to have a .cbz extension.
        Assume that renaming is enough to convert
        Updates self.input_file to point to the new file.
        """
        base, _ = os.path.splitext(self.input_file)
        new_path = base + ".cbz"
        os.rename(self.input_file, new_path)
        logger.info(f"Renamed {self.input_file} to {new_path}")
        self.input_file = new_path
    
    def modify_opf_and_repack(self, output_folder=None):
        """
        Unzips the EPUB, injects a <meta> tag into the .opf file,
        and repacks the EPUB. If output_folder is None, overwrite the original file.
        """
        epub_path = Path(self.input_file)
        folder_name = epub_path.parent.name

        if output_folder:
            output_folder = Path(output_folder)
            output_folder.mkdir(parents=True, exist_ok=True)
            new_epub_path = output_folder / epub_path.name
        else:
            new_epub_path = epub_path

        with tempfile.TemporaryDirectory() as extract_dir:
            extract_path = Path(extract_dir)
            with zipfile.ZipFile(epub_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            # Find the .opf file
            opf_file = next(extract_path.rglob("*.opf"), None)
            if not opf_file:
                logger.info(f"No OPF file found in EPUB: {epub_path}")
                return

            logger.info(f"Found OPF file: {opf_file}")

            # Parse and modify the OPF file
            tree = ET.parse(opf_file)
            root = tree.getroot()

            # Define metadata
            metadata = root.find("metadata")
            if metadata is None:
                logger.info("No <metadata> tag found in OPF. Creating one.")
                # Determine where to insert it — usually directly under <package>
                metadata = ET.Element('metadata')
                root.insert(0, metadata)  # Insert at the beginning

            # Inject new <meta> tag
            meta_element = ET.Element('meta')
            meta_element.set('name', 'calibre:series')
            meta_element.set('content', folder_name)
            metadata.append(meta_element)

            # Save the updated OPF file
            tree.write(opf_file, encoding='utf-8', xml_declaration=True)

            # Repackage EPUB
            with zipfile.ZipFile(new_epub_path, 'w', zipfile.ZIP_DEFLATED) as new_epub:
                for file_path in extract_path.rglob('*'):
                    arcname = file_path.relative_to(extract_path)
                    new_epub.write(file_path, arcname)

            logger.info(f"Modified EPUB saved to: {new_epub_path}")