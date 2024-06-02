
import requests
from bs4 import BeautifulSoup
import os
import json
import pandas as pd
import re

from models import Pokemon, Tier, TierList



def split_html_by_headers(html_content, header_tag, class_type=None):
    soup = BeautifulSoup(html_content, 'html.parser')

    if class_type:
        sections = soup.find_all(header_tag, class_=class_type)
    else:
        sections = soup.find_all(header_tag)

    result = []
    for section in sections:
        header_text = section.get_text()
        content = ''
        for sibling in section.find_next_siblings():
            if sibling.name == header_tag:
                break
            content += str(sibling)

        result.append({
            'name': header_text,
            'content': content
        })

    return result


def split_by_div(html_content, div_class):
    soup = BeautifulSoup(html_content, 'html.parser')
    sections = soup.find_all('div', class_=div_class)
    result = []

    for section in sections:
        content = section.decode_contents()  # Get the inner HTML of the div
        result.append({
            'name': section.get('data-title', 'No title'),
            'content': content
        })

    return result

def associate_tier_with_pokemon(html_content, tier_class, pokemon_class):
    tier_splits = split_html_by_headers(html_content, 'h2', class_type=tier_class)
    result = []

    for tier in tier_splits:
        tier_name = tier['name']
        pokemon_list = split_by_div(tier['content'], pokemon_class)
        for pokemon in pokemon_list:
            pokemon['tier'] = tier_name
            result.append(pokemon)

    return result



# Function to extract the form value
def extract_forme_value(pokemon_string):
    # Define the regular expression pattern
    pattern = r'\((\w+) Forme?\)'
    match = re.search(pattern, pokemon_string)
    if match:
        return match.group(1)
    else:
        return None

# Function to strip the form value
def strip_forme(pokemon_string):
    pattern = r'\(\w+ Forme?\)'
    stripped_string = re.sub(pattern, '', pokemon_string, flags=re.IGNORECASE).strip()
    return stripped_string

def convert_name(pokemon_name):
    pokemon_name_output = pokemon_name.upper()
    form = False
    if "Mega" in pokemon_name:
        if " Y" in pokemon_name:
            pokemon_name_output = pokemon_name_output + "_MEGA_Y"
        elif " X" in pokemon_name:
            pokemon_name_output = pokemon_name_output + "_MEGA_X"
        else:
            pokemon_name_output = pokemon_name_output + "_MEGA"
        pokemon_name_output = pokemon_name_output + "_MEGA"
        form = False
    elif "Hisuian" in pokemon_name:
        pokemon_name_output =  pokemon_name_output.replace("HISUIAN", "") + "_HISUIAN"
        form = True
    if "Alolan" in pokemon_name:
        pokemon_name_output = pokemon_name_output.replace("ALOLAN", "") + "_ALOLAN"
        form = True
    if "Galarian" in pokemon_name:
        pokemon_name_output = pokemon_name_output.replace("GALARIAN", "") + "_GALARIAN"
        form = True
    if "Form" in pokemon_name:
        form_type = extract_forme_value(pokemon_name)
        print(f"Form Type: {form_type}")
        pokemon_name_output = strip_forme(pokemon_name_output) + f"_{form_type.upper()}"
        form = True
    if "Shadow" in pokemon_name:
        pokemon_name_output = pokemon_name_output.replace("SHADOW", "") + "_SHADOW"
        form = True
    if "(Confined)" in pokemon_name: # Hoopa (Confined)
        pokemon_name_output = pokemon_name_output.replace("(CONFINED)", "") + "_CONFINED"
        form = True
    if "(Unbound)" in pokemon_name: # Hoopa (Unbound)
        pokemon_name_output = pokemon_name_output.replace("(Unbound)", "") + "_UNBOUND"
        form = True
    
    if form:
        pokemon_name_output = pokemon_name_output + "_FORM"

    pokemon_name_output = pokemon_name_output.replace("'", "") # e.g. Sirfetch'd to SIRFETCHD
    return pokemon_name_output

if __name__ == "__main__":

    # cache https://fight.pokebattler.com/pokemon
    if os.path.exists('pokemon_battle_data.json'):
        print("Using cached pokemon battle data")
        with open('pokemon_battle_data.json', 'r') as f:
            # open as json
            pokemon_battle_data = json.load(f)
    else:
        print("Downloading pokemon battle data")
        pokemon_battle_data = requests.get("https://fight.pokebattler.com/pokemon")
        pokemon_battle_data.raise_for_status()
        # save to json file for caching purposes
        with open('pokemon_battle_data.json', 'w') as f:
            # pretty print json
            f.write(json.dumps(pokemon_battle_data.json(), indent=4))

    # load the pokemon battle data into a pandas dataframe
    pokemon_battle_data = pd.DataFrame(pokemon_battle_data["pokemon"])

    url = "https://gamepress.gg/pokemongo/attackers-tier-list"
    response = requests.get(url)
    response.raise_for_status()
    #print(response.text)

    # Split page so that it fits in context
    #loader = UnstructuredHTMLLoader(response.text) # TODO: How to use this and chain it to a text splitter?
    tier_pokemon_list = associate_tier_with_pokemon(response.text, 'main-title', 'tier-list-cell-row')
    pokemon_structured_list = []
    for pokemon in tier_pokemon_list:
        
        print(f"Tier: {pokemon['tier']}")
        print(f"Name: {pokemon['name']}")
        # if pokemon name contains shadow
        
        pokemon_name_converted = convert_name(pokemon['name'])
        print(f"Converted Name: {pokemon_name_converted}")
        print("---")

    # save the structured data to pickle file
    import pickle
    with open('pokemon_structured_data.pkl', 'wb') as f:
        pickle.dump(pokemon_structured_list, f)

    # # load the structured data from pickle file
    # with open('pokemon_structured_data.pkl', 'rb') as f:
    #     pokemon_structured_list = pickle.load(f)

    # print the structured data
    for pokemon in pokemon_structured_list:
        print(pokemon)
        print("---")