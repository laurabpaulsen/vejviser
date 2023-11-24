from pathlib import Path
import re
import pandas as pd
from tqdm import tqdm
import re
from multiprocessing import Pool, cpu_count

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

    
def process_match(text):
    potential_occupation = re.split(' |\n', text)
    
    if potential_occupation[-1] == "":
        potential_occupation = potential_occupation[-2]
    
    else:
        potential_occupation = potential_occupation[-1]
    
    return potential_occupation


def extract_potential_occupations(txt, year):
    # Replace all new lines with spaces
    #txt = txt.replace("\n", " ")

    # Replace more than one space with one space
    txt = re.sub(r"\s+", " ", txt)


    
    if year == 1880:
        pass

    if year == 1900:
        pass

    if year == 1930:
        pass

    if year == 1990:
        # Find all phone numbers
        search_pattern = r" \d{2} ?\d{2} ?\d{2} ?\d{2}"

    if year == 1945:
        # Look for each of these characters $, &, £, can be followed by space or Da
        search_pattern = r"[$&£](?: |Da)"

    # Find all match start positions
    match_positions = [match.start() for match in re.finditer(search_pattern, txt)]

    # create a list split on all the match start positions
    parts = [txt[i:j] for i,j in zip(match_positions, match_positions[1:]+[None])]
    
    potential_occupations = [process_match(part) for part in parts]

    return potential_occupations


def clean_occupation_list(occupations, create_occupation_list = True, remove_list = []):
    """
    Removes duplicates and occupations that are in the names list
    """
    # A few street names were captured as well
    occupations = [occupation for occupation in occupations if not occupation.isupper()]

    # lower case
    occupations = [occupation.lower() for occupation in occupations]
    
    # remove if in remove list
    occupations = [occupation for occupation in occupations if occupation not in remove_list]
    
    # remove if there is a number in it
    occupations =  [occupation for occupation in occupations if not any(char.isdigit() for char in occupation)]

    # replace commas in with nothing 
    occupations = [occupation.replace(",", ".") for occupation in occupations]

    # remove if special characters is present (except for . and -)
    occupations = [occupation for occupation in occupations if not re.search(r'[^a-zA-Z0-9.-]', occupation)]
    
    ### NOTE: CHECK THAT THE FOLLOWING ARE NOT PROBLEMS FOR COUNT_OCCUPATIONS ###
    # remove spaces
    occupations = [occupation.replace(" ", "") for occupation in occupations]

    # remove . if they are at the end!
    #occupations = [occupation.rstrip('.') for occupation in occupations]

    # remove if length is two or shorter
    occupations = [occupation for occupation in occupations if len(occupation) > 2]
    

    if create_occupation_list:
        occupations = list(set(occupations))


    return sorted(occupations)



if __name__ in "__main__":
    path = Path(__file__).parent

    # load in the extracted text files from vejvisere
    txt_path = path / "extracted_text"

    txts, years = load_txt(txt_path)

    # load in csv of names
    names_path = path / "misc" / "name_gender.csv"
    names = pd.read_csv(names_path)["Name"].to_list()

    # read in txt file with last names
    last_names_path = path / "misc" / "Efternavne - alle.txt"
    last_names = open(last_names_path, "r", encoding="UTF-8").read().split("\n")

    # read in txt file with danish stop words
    stop_word_path = path / "misc" / "stopord.txt"
    stop_words = open(stop_word_path, "r", encoding="UTF-8").read().split("\n")
    
    remove_list = names + last_names + stop_words + ["side"]

    remove_list = [name.lower() for name in remove_list]
    
    occupations = []
    
    for i, (txt, year) in enumerate(zip(txts, years)):
        print(f"Extracting occupations from file number {i+1}")
        potential_occupations = extract_potential_occupations(txt, int(year))
        occupations.extend(potential_occupations)


    occupations = clean_occupation_list(occupations, remove_list = remove_list)

    print(f"Number of potential occupations: {len(occupations)}")

    # save the potential occupations to a csv file
    occupations_path = path / "occupation_list.csv"

    pd.DataFrame(occupations, columns=["occupation"]).to_csv(occupations_path, index=False)