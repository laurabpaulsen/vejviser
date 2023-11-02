import os
from pathlib import Path
import pandas as pd
import re
from collections import Counter

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

    # create master data frame
    data = pd.DataFrame( {'year': None, 'street': None, 'occupations': None, 'count': None} )

    txts_in = list_txts_dir(txts_path)

    for txt_in in txts_in:

        with open(txt_in, "r", encoding='latin-1') as file:
            txt = file.read()
        
        splitted = re.split(' |\n', txt)

        dictionary = extract_streets(splitted)

        for i, idx in enumerate(dictionary['index']):

            next_street_index = dictionary['index'][i+1]
            text_chunk = splitted[idx:next_street_index]
            dictionary['text'].append(text_chunk)

        for i, text in enumerate(dictionary['text']):

            # extract occupations
            occupations = [token for token in text if token in occupation_list]
        
            # count occupations for each street
            occupations_count = Counter(occupations)

            # organize in df
            df = pd.DataFrame({
                "year": [os.path.splitext(txt_in)[0]] * len(occupations_count),
                "street": [data["street"][i]] * len(occupations_count),
                "occupations": [item[0] for item in occupations_count.items()],
                "count":       [item[1] for item in occupations_count.items()]
                })

            data = pd.concat([data, df], ignore_index=True, axis=0)

        # create ndjson
        data_json = data.to_json(orient='records', lines=True)

        out_path = path / "out" / "street_occupations.ndjson"
        with open(out_path, "w", encoding="latin-1") as file:
            file.write(data_json)
