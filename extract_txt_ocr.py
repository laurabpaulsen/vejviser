import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
from pathlib import Path


def list_pdfs_dir(path: Path):
    """
    Lists all the pdfs in a given path, both in the root and in subfolders.
    
    Parameters
    ----------
    path : Path
        Path to the folder containing the pdfs.
    
    Returns
    -------
    pdfs : list
        List of all the pdfs in the given path.
    """
    pdfs = []
    for pdf in path.glob('**/*.pdf'):
        pdfs.append(pdf)
    
    return pdfs


if __name__ in "__main__":
    path = Path(__file__).parent

    pdfs_path = path / "pdfs" / "page0064.pdf"
    out_path = path / "extracted_txt"

    # get all pdfs in the folder
    pdfs = list_pdfs_dir(pdfs_path)

    for pdf in pdfs:
        
        # convert pdf to image
        doc = convert_from_path(pdf)

        txt_all = ""

        for page_number, page_data in enumerate(doc):
            page_data = np.asarray(page_data)
            txt = pytesseract.image_to_string(Image.fromarray(page_data), lang='dan')
            
            txt_all = " ".join([txt_all, txt])

        with open(out_path / f"{pdf.stem}.txt", "w") as text_file:
                text_file.write(txt_all)