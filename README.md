# vejviser
This repository holds the code for using OCR to extract text from images danish street registers and investigating the occupations of the people living in the streets.

## Pipeline
1. Clone the repository
2. Run `setup_env.sh` to create a virtual environment and install the required packages
3. Extract text from the images using OCR 
```
extract_txt_ocr.py
```
4. Create a list of occupations from the extracted text by identifiying words before phone numbers. After this step, the list of occupations is cleaned by removing names and digits.
```
create_occupation_list.py
```
5. Go through the extracted texts. For each street the occupations are counted. The results are saved to a csv file.
```
count_occupations.py # NOT IMPLEMENTED YET
```


## Repository structure
The repository is structured as follows:
```
.
├── extracted_text              # not included in repository
├── misc                        # not included in repository
├── pdfs                        # not included in repository
├── create_occupation_list.py   creates a list of occupations from the extracted text
├── extract_txt_ocr.py          extracts text from images using OCR
├── README.md
├── requirements.txt
├── setup_env.sh

```