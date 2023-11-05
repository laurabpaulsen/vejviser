import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
from pathlib import Path
from tqdm import tqdm

def list_pdfs_dir(path: Path):
    """
    Lists all the pdfs in a given path.
    
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

    pdfs_path = path / "pdfs" 
    out_path = path / "extracted_text"

    if not out_path.exists():
        out_path.mkdir()

    # get all pdfs in the folder
    pdfs = list_pdfs_dir(pdfs_path)

    for pdf in tqdm(pdfs, desc = "Extracting text from pdf"):
        
        # convert pdf to image
        doc = convert_from_path(pdf)

        txt_all = ""

        for page_number, page_data in tqdm(enumerate(doc)):
            page_data = np.asarray(page_data)
            txt = pytesseract.image_to_string(Image.fromarray(page_data), lang='dan')
            
            txt_all = " ".join([txt_all, txt])

        with open(out_path / f"{pdf.stem}.txt", "w", encoding="UTF-8") as text_file:
                text_file.write(txt_all)