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
count_occupations.py # draft, check with Peter that the output format is as expected
```

## Current state of the project
**A proof-of-concept has been created only looking at data only from 1945 and 1990 (both the file A-K and L-Å).**

* We can extract what we deem "potential occupations" by grabbing the word before a phone number for the data from 1990. However, some times no occupation is included, and then we end up getting a last name or some other messy stuff

* For the data from 1945 it is more complicated as there is a "funny" character (that I have no clue what is) just after the occupation. When we are extracting the text, this character is interpreted as many different characters ($, &, £, etc)

* To try and clean it up as best as we can, we are taking a list of danish names (both first and last) as well as a list of stopwords, and if the "occupation" is in that list we remove it. Furthermore we remove any "occupations" that are just containing numbers

* We then use this list as a "look up" in the Gaderegister, and count the number of times each occupation is mentioned in the text related to each street. 

**Results of running the proof-of-concept**

We are able to extract occupations from the pdfs. In total, our script has extracted 31726 unique tokens of which many are not actual occupations. Below, we show the relative frequency of the 30 most common occupations across the entire city for one year. Evidently, we have problems with non-occupations being included in our occupation list, e.g., "eee" and "alfabetiseringsregler". 

![](out/plot.png)

**Future steps**
* The strategy of looking at the word before the phone number or $, & and £ to capture occupations does not work for all the data. As the structure varies a lot, it will pretty much take individual search patterns for each year to try and get all the occupations. 

* Even with year-specific extraction rules/patterns, we still end up catching a lot of non-occupations, and the list will require manual cleaning before we use it as a look up. 

* We need to know at what page in the pdf (not the number at the bottom of the page, but the pdf page number) the actual gade-register starts. We also need to know where it ends. See `file_info.py` and `file_info.txt`.

* When trying to extract texts from older registers, we are experiencing issues with the quality.

* We most likely do not catch all occupations in the pdfs. This can be due to several things: The quality of the extracted text (e.g., if "bager" is extracted as "bag er" or the tokens to be matched with the year-specific pattern are not extracted correctly with OCR), if an occupation is also a name, if the year-specific pattern does not match all intended cases.

* Some occupations might be captured by different spellings. To merge these we would need to make some kind of mapping. 

* The way we determine when we have reached a new street seems to work well for several years. However, this should be thoroughly tested. 


**Suggestion to check accuracy of our approach**
* Manually create a count of occupations in some select pages (preferably done for a range of years)
* Compare that to the result of running our pipeline
* Investigate where it fails (e.g., extracting text with OCR, the list of occupations we are searching for, when we are using the list to count the number of each occupation in a given street)



## Repository structure
The repository is structured as follows:
```
.
├── extracted_text              # not included in repository
├── misc                        # not included in repository
├── pdfs                        # not included in repository
├── out                         # not included in repository
├── create_occupation_list.py   creates a list of occupations from the extracted text
├── extract_txt_ocr.py          extracts text from images using OCR
├── README.md
├── requirements.txt
├── setup_env.sh

```
