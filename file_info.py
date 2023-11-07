"""
This script creates a dictionary of file information for the files in the pdfs folder.

It holds the start and stop page numbers for each file, as well as the file name.
"""
from pathlib import Path
import json

if __name__ in "__main__":
    path = Path(__file__).parent

    # dictionary of file names and their start and stop pages
    file_info = {
        # 'file_name': [start_page, stop_page]
        "kraks vejviser 1990 gaderegister A-K.pdf": [62, 918],
        "kraks vejviser 1990 gaderegister L-Å.pdf": [2, 933],
        'Kraks Vejviser 1945 gaderegister .pdf': [27, None],
    }

    # save the dictionary to a file
    with open(path / 'file_info.txt', 'w') as f:
        json.dump(file_info, f)


