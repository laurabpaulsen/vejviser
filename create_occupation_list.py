from pathlib import Path
import re
import pandas as pd

def load_concat_txt(path):
    """
    Loads and concatenates all txt files in a directory

    Args:
        Path: path to directory

    Returns:
        str: concatenated txt files
    """

    # get all txt files in the directory
    txt_files = [file for file in path.glob("*.txt")]

    # load in all txt files
    txt_files = [open(txt_file, "r", encoding="UFT-8").read() for txt_file in txt_files]

    # concatenate all txt files
    txt_files = " ".join(txt_files)

    return txt_files


def extract_potential_occupations(txt):
    """
    Extracts the potential occupations.
    
    Notes: Occupations preceeds the phone number in a format XX XX XX XX. Sometimes no occupation is included, therefore the output from this function need further cleaning.
    """

    # replace all new lines with spaces
    txt = txt.replace("\n", " ")

    # replace more than one space with one space
    txt = re.sub(r"\s+", " ", txt)

    # find all phone numbers
    phone_numbers = re.findall(r"\d{2} \d{2} \d{2} \d{2}", txt)
    

    # find all the potential occupations
    potential_occupations = []

    for phone_number in phone_numbers:
        split_phone_number = txt.split(phone_number)[0] # keeping what is before the phone number 

        # split on space
        potential_occupation = split_phone_number.split(" ")
        
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
    txt_path = path / "extracted_txt"

    txts = load_concat_txt(txt_path)


    potential_occupations = extract_potential_occupations(txts)

    # remove duplicates
    potential_occupations = list(set(potential_occupations))

    # load in csv of names
    names_path = path / "misc" / "name_gender.csv"
    names = pd.read_csv(names_path)["Name"].to_list()

    potential_occupations = clean_occupation_list(potential_occupations, names)


    print(f"Number of potential occupations: {len(potential_occupations)}")
    print(potential_occupations)


    # save the potential occupations to a csv file
    occupations_path = path / "occupation_list.csv"

    pd.DataFrame(potential_occupations, columns=["occupation"]).to_csv(occupations_path, index=False)