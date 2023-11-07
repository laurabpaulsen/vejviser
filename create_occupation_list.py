from pathlib import Path
import re
import pandas as pd

def load_txt(path):
    """
    Loads txts files from a directory and adds them to a list. Furthermore a list with the year of the txt files is created.
    Args:
        Path: path to directory

    Returns:
        txt_files: list with txt files
        years: list with years
    """

    # get all txt files in the directory
    txt_paths = [file for file in path.glob("*.txt")]

    # get the year of the txt files using regex looking for 4 digits
    years = [re.findall(r"\d{4}", str(path))[0] for path in txt_paths]

    # load in all txt files
    txt_files = [open(txt_path, "r", encoding="UTF-8").read() for txt_path in txt_paths]

    return txt_files, years



def extract_potential_occupations(txt:str, year:int):
    """
    Extracts the potential occupations.
    """

    # replace all new lines with spaces
    txt = txt.replace("\n", " ")

    # replace more than one space with one space
    txt = re.sub(r"\s+", " ", txt)

    if year >= 1990:
        # find all phone numbers
        search_pattern = r"\d{2} \d{2} \d{2} \d{2}"

    if year == 1945:
        # look for each of these characters $, &, £, can be followed by space or Da
        search_pattern = r"[$&£](?: |Da)"

    # get the indexes of the matches
    matches = re.finditer(search_pattern, txt)
    
    potential_occupations = []

    for match in matches:
        split_txt = txt[:match.start()]

        # split on space
        potential_occupation = split_txt.split(" ")
        
        # get the last element if it is not empty else get the second last element
        if potential_occupation[-1] == "":
            potential_occupation = potential_occupation[-2]
        else:
            potential_occupation = potential_occupation[-1]

        potential_occupations.append(potential_occupation)

    return potential_occupations

def clean_occupation_list(occupations, remove_list = []):
    """
    Removes duplicates and occupations that are in the names list
    """

    occupations = list(set(occupations))

    # remove if in remove list
    occupations = [occupation for occupation in occupations if occupation not in remove_list]

    # remove if it is a number
    occupations = [occupation for occupation in occupations if not occupation.isnumeric()]

    return occupations


    


if __name__ in "__main__":
    path = Path(__file__).parent

    # load in the extracted text files from vejvisere
    txt_path = path / "extracted_text"

    txts, years = load_txt(txt_path)

    occupations = []
    
    for txt, year in zip(txts, years):
        potential_occupations = extract_potential_occupations(txt, int(year))
        occupations.extend(potential_occupations)

    # remove duplicates
    occupations = list(set(occupations))

    # load in csv of names
    names_path = path / "misc" / "name_gender.csv"
    names = pd.read_csv(names_path)["Name"].to_list()

    occupations = clean_occupation_list(occupations, names)


    print(f"Number of potential occupations: {len(occupations)}")
    print(occupations)


    # save the potential occupations to a csv file
    occupations_path = path / "occupation_list.csv"

    pd.DataFrame(occupations, columns=["occupation"]).to_csv(occupations_path, index=False)