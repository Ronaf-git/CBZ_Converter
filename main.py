# main.py
from functions import *
from classes import *

def main(root_folder):
    log_file = os.path.join(root_folder, "app.log")
    setup_logger('global_logger',log_file)  # Set up the global logger
    convert_comics_in_folder_to_cbz(root_folder)
    add_ComicInfoXML_to_CBZ_Recurse(root_folder)

if __name__ == "__main__":
    root_folder = r"Your\Path" 

    main(root_folder)
