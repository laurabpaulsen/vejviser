import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import re
from pathlib import Path


def list_pdfs_dir(path):
    """
    Lists all the pdfs in a given path
    """
    pass


if __name__ in "__main__":
    path = Path(__file__).parent

    pdfs_path = path / "pdfs" / "page0064.pdf"
    out_path = path / "extracted_txt"

    # Convert pdf to image
    doc = convert_from_path(pdfs_path)

    txt_all = ""

    for page_number, page_data in enumerate(doc):
        page_data = np.asarray(page_data)
        txt = pytesseract.image_to_string(Image.fromarray(page_data), lang='dan')
        
        txt_all = " ".join([txt_all, txt])
        

    with open(out_path / "test.txt", "w") as text_file:
            text_file.write(txt_all)