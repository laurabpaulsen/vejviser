import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
from pathlib import Path
from tqdm import tqdm
import json


if __name__ in "__main__":
    path = Path(__file__).parent

    pdfs_path = path / "pdfs" 
    out_path = path / "extracted_text"

    if not out_path.exists():
        out_path.mkdir()

    # load the file info
    with open(path / 'file_info.txt', 'r') as f:
        file_info = json.load(f)


    for pdf, info in tqdm(file_info, desc = "Extracting text from pdf"):
        # get the start and stop page numbers for the file
        start_page = info[0]
        stop_page = info[1]

        # check if the file has already been processed
        if (out_path / f"{pdf.stem}.txt").exists():
            continue
        
        # convert pdf to image
        doc = convert_from_path(pdfs_path / pdf, first_page=start_page, last_page=stop_page)

        txt_all = ""

        for page_number, page_data in tqdm(enumerate(doc)):
            page_data = np.asarray(page_data)
            txt = pytesseract.image_to_string(Image.fromarray(page_data), lang='dan')
            
            txt_all = " ".join([txt_all, txt])

        with open(out_path / f"{pdf.stem}.txt", "w", encoding="UTF-8") as text_file:
                text_file.write(txt_all)