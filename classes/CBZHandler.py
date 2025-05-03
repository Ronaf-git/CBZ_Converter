import os
import zipfile
import io
import re
from lxml import etree
from .ComicBookHandler import *


import os
import re
import zipfile
from lxml import etree
import io
import logging

logger = logging.getLogger(__name__)

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

    def update_comic_info_xml(self, existing_comic_info):
        """Update specific nodes in the existing ComicInfo.xml."""
        root = etree.fromstring(existing_comic_info)

        # Update or add Series and LocalizedSeries nodes
        series_elem = root.find("Series")
        localized_series_elem = root.find("LocalizedSeries")
        
        if series_elem is None:
            series_elem = etree.SubElement(root, "Series")
        if localized_series_elem is None:
            localized_series_elem = etree.SubElement(root, "LocalizedSeries")

        series_elem.text = self.folder_name
        localized_series_elem.text = self.folder_name
        
        # Update Volume and Number nodes if present
        if self.vol_number:
            volume_elem = root.find("Volume")
            if volume_elem is None:
                volume_elem = etree.SubElement(root, "Volume")
            volume_elem.text = self.vol_number
        
        if self.ch_number:
            number_elem = root.find("Number")
            if number_elem is None:
                number_elem = etree.SubElement(root, "Number")
            number_elem.text = self.ch_number
        
        buf = io.BytesIO()
        tree = etree.ElementTree(root)
        tree.write(buf, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        buf.seek(0)
        return buf

    def add_comic_info_to_cbz(self):
        """Add or update ComicInfo.xml in the CBZ file."""
        temp_cbz_path = self.cbz_file + ".temp"
        
        with zipfile.ZipFile(self.cbz_file, 'r') as zip_ref:
            with zipfile.ZipFile(temp_cbz_path, 'w', zipfile.ZIP_DEFLATED) as zip_write:
                comic_info_updated = False
                for item in zip_ref.infolist():
                    if item.filename == 'ComicInfo.xml':
                        # If ComicInfo.xml exists, update the content
                        with zip_ref.open(item.filename) as comic_info_file:
                            existing_comic_info = comic_info_file.read()
                            updated_comic_info = self.update_comic_info_xml(existing_comic_info)
                            zip_write.writestr('ComicInfo.xml', updated_comic_info.read())
                        comic_info_updated = True
                    else:
                        # Copy other files without changes
                        zip_write.writestr(item, zip_ref.read(item.filename))

                if not comic_info_updated:
                    # If ComicInfo.xml doesn't exist, add it
                    comic_info_buf = self.create_comic_info_xml()
                    zip_write.writestr('ComicInfo.xml', comic_info_buf.read())

        os.replace(temp_cbz_path, self.cbz_file)
        logger.info(f"Updated ComicInfo.xml inside {self.cbz_file}")
