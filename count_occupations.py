from pathlib import Path
import pandas as pd
import re
from collections import Counter
from create_occupation_list import clean_occupation_list

def list_txts_dir(path: Path):
    """
    Lists all the txts in a given path.
    
    Parameters
    ----------
    path : Path
        Path to the folder containing the txts.
    
    Returns
    -------
    txts : list
        List of all the txts in the given path.
    """
    txts = []
    for txt in path.glob('*.txt'):
        txts.append(txt)
    
    return txts

def extract_streets(splitted: list):
    """
    Identifies the street names and their locations in the string.
    
    Parameters
    ----------
    splitted : list
        The splitted string representing an entire catalog for a given year.
    
    Returns
    -------
    dictionary : dict
        Dictionary with four keys - street, index (of first street name token in splitted), and text. 
        Only street and index are filled in this function
    """

    post_code_pattern = re.compile("^\d{4}$")
    
    keys = ['street','index','text']
    dictionary = {key: [] for key in keys}

    for idx, token in enumerate(splitted):
        
        # grap tokens that are upper case and followed by a post code
        if token.isupper() and token.isalpha() and post_code_pattern.search(splitted[idx+1]):

            test_indices = range(idx-5, idx+1)
            street = [splitted[i] for i in test_indices if splitted[i].isalpha() and splitted[i].isupper()]
            street_index = idx-len(street)+1
            street = " ".join(street)

            dictionary['street'].append(street)
            dictionary['index'].append(street_index)

    return dictionary



if __name__ in "__main__":
    
    path = Path(__file__).parent

    txts_path = path / "extracted_text" 

    occupation_list = pd.read_csv( path / "occupation_list.csv")

    # DELETE OR EDIT ONCE TRUE OCCUPATION_LIST IS AVAILABLE
    occupation_list = list(occupation_list['occupation'] )

    # create master data frame
    data = pd.DataFrame(columns = ['year', 'street', 'occupations', 'count'])
    
    txts_in = list_txts_dir(txts_path)

    n_txts = len(txts_in)
    txt_counter = 0

    for txt_in in txts_in:

        txt_counter += 1
        print(f"[INFO]: Processing text {txt_counter} of {n_txts}")

        with open(txt_in, "r", encoding='UTF-8') as file:
            txt = file.read()
        
        splitted = re.split(' |\n', txt)

        dictionary = extract_streets(splitted)

        # add corresponding text to each street in dictionary
        for i, idx in enumerate(dictionary['index']):

            if i == len(dictionary['index'])-1:
                next_street_index = None
            else:
                next_street_index = dictionary['index'][i+1]
            text_chunk = splitted[idx:next_street_index]
            dictionary['text'].append(text_chunk)

        for i, text in enumerate(dictionary['text']):

            # preprocess text so it matches what is done in create_occupation list
            text_cleaned = clean_occupation_list(text, create_occupation_list=False, remove_list=[])

            # extract occupations
            occupations = [token for token in text if token in occupation_list]
        
            # count occupations for each street
            occupations_count = Counter(occupations)

            # organize in df
            df = pd.DataFrame({
                "year": [re.findall(r"\d{4}", str(txt_in))[0]] * len(occupations_count),
                "street": [dictionary['street'][i]] * len(occupations_count),
                "occupations": [item[0] for item in occupations_count.items()],
                "count":       [item[1] for item in occupations_count.items()]
                })

            data = pd.concat([data, df], ignore_index=True, axis=0)

    

    # create ndjson
    data_json = data.to_json(orient='records', lines=True)

    out_path = path / "out" 
    data.to_csv(path / "out" / "street_occupations.csv", index = False)
    
    if not out_path.exists():
        out_path.mkdir()
    
    with open(out_path / "street_occupations.ndjson", "w", encoding="UTF-8") as file:
        file.write(data_json)

