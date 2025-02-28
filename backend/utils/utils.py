from datetime import datetime
import os
from PIL import Image
from PIL.ExifTags import TAGS

from globals import MEME_DIRECTORY

def get_os_meme_path(img_path: str) -> str:
    return f"{MEME_DIRECTORY}/{img_path.strip('/')}"

# Function to get EXIF data
def get_exif_data(image_path:str):
    _image_path = get_os_meme_path(image_path)
    # Open the image file
    image = Image.open(_image_path)
    
    # Extract EXIF data
    exif_data = image._getexif() if hasattr(image,"_getexif") else None
    
    # Convert EXIF data to human-readable format
    exif_dict = {}
    if exif_data is not None:
        for tag, value in exif_data.items():
            tag_name = str(TAGS.get(tag, tag))
            exif_dict[tag_name] = value if type(value) in ["str", "int", "float"] else str(value)
            
    return exif_dict

def get_file_dates(image_path:str):
    _image_path = get_os_meme_path(image_path)
    # Get file creation and modification dates
    file_stats = os.stat(_image_path)
    creation_date = file_stats.st_ctime  # Creation date
    modification_date = file_stats.st_mtime  # Modification date

    creation_date_readable = datetime.fromtimestamp(creation_date)
    modification_date_readable = datetime.fromtimestamp(modification_date)
    
    return creation_date_readable, modification_date_readable