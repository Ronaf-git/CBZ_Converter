import os
import zipfile
import io
import re
from lxml import etree
from .ComicBookHandler import *


class CBZHandler:
    def __init__(self, cbz_file):
        """Check if CBZ"""
        if not os.path.exists(cbz_file):
            raise FileNotFoundError(f"The input file {cbz_file} does not exist.")
        if not cbz_file.lower().endswith('.cbz'):
            raise ValueError(f"The file {cbz_file} is not a valid cbz file.")
    
        """Initialize with the CBZ file path."""
        self.cbz_file = cbz_file
        self.folder_name = os.path.basename(os.path.dirname(self.cbz_file))
        self.folder_name = re.sub(r'\s*\[.*?\]\s*|\(.*?\)', '', self.folder_name).strip()
        self.vol_number, self.ch_number = self.extract_vol_and_ch()
        
    def extract_vol_and_ch(self):
        """Extract volume and chapter numbers from the file name."""
        vol_match = re.search(r'(Vol\.?|Volume\s*|T\s*|Tome\s*)(\d+)', os.path.basename(self.cbz_file), re.IGNORECASE)
        vol_number = vol_match.group(2) if vol_match else None

        ch_match = re.search(r'(ch\.?|Chapter\.?|Chapitre\.?)\s*(\d+)', os.path.basename(self.cbz_file), re.IGNORECASE)
        ch_number = ch_match.group(2) if ch_match else None

        return vol_number, ch_number

    def create_comic_info_xml(self):
        """Create the ComicInfo.xml content."""
        root = etree.Element("ComicInfo")
        etree.SubElement(root, "Series").text = self.folder_name
        etree.SubElement(root, "LocalizedSeries").text = self.folder_name
        if self.vol_number:
            etree.SubElement(root, "Volume").text = self.vol_number
        if self.ch_number:
            etree.SubElement(root, "Number").text = self.ch_number

        buf = io.BytesIO()
        tree = etree.ElementTree(root)
        tree.write(buf, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        buf.seek(0)
        return buf

    def add_comic_info_to_cbz(self):
        """Add ComicInfo.xml to the CBZ file."""
        comic_info_buf = self.create_comic_info_xml()
        temp_cbz_path = self.cbz_file + ".temp"

        with zipfile.ZipFile(self.cbz_file, 'r') as zip_ref:
            with zipfile.ZipFile(temp_cbz_path, 'w', zipfile.ZIP_DEFLATED) as zip_write:
                comic_info_added = False
                for item in zip_ref.infolist():
                    if item.filename == 'ComicInfo.xml':
                        zip_write.writestr('ComicInfo.xml', comic_info_buf.read())
                        comic_info_added = True
                    else:
                        zip_write.writestr(item, zip_ref.read(item.filename))

                if not comic_info_added:
                    zip_write.writestr('ComicInfo.xml', comic_info_buf.read())

        os.replace(temp_cbz_path, self.cbz_file)
        logger.info(f"Updated ComicInfo.xml inside {self.cbz_file}")
