import instructor.exceptions
from openai import OpenAI
from pydantic import BaseModel
import instructor
import requests
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_text_splitters import HTMLHeaderTextSplitter
from bs4 import BeautifulSoup

from models import Pokemon, Tier, TierList

# enables `response_model` in create call
client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:8080/v1",
        api_key="ollama",  # required, but unused
    ),
    mode=instructor.Mode.JSON
)


url = "https://gamepress.gg/pokemongo/attackers-tier-list"
response = requests.get(url)
response.raise_for_status()
#print(response.text)

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

# Split page so that it fits in context
#loader = UnstructuredHTMLLoader(response.text) # TODO: How to use this and chain it to a text splitter?

tier_pokemon_list = associate_tier_with_pokemon(response.text, 'main-title', 'tier-list-cell-row')
pokemon_structured_list = []
for pokemon in tier_pokemon_list:
    print(f"Tier: {pokemon['tier']}")
    print(f"Name: {pokemon['name']}")
    # print(f"Content: {pokemon['content']}")
    # print("---")

    try:
        pokemon_structured = client.chat.completions.create(
            model="function-calling",
            messages=[
                {
                    "role": "user",
                    "content": f"Extract the pokemon:  Tier: {pokemon['tier']}, Name: {pokemon['name']}, content: {pokemon['content']}",
                }
            ],
            response_model=Pokemon,
            max_retries=10
        )

    except instructor.exceptions.InstructorRetryException  as e:
        print(e)
        print(e.n_attempts)
        print(e.last_completion)

    print(pokemon_structured)
    pokemon_structured_list.append(pokemon_structured)

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