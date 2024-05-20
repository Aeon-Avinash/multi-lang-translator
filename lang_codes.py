import requests
from bs4 import BeautifulSoup
import json

def generate_lang_code_file():
    # URL of the Flores README containing the language codes
    url = 'https://raw.githubusercontent.com/openlanguagedata/flores/main/README.md'

    # Fetch the page content
    response = requests.get(url)
    content = response.text

    # Extract the table content by parsing the plain text
    lines = content.split('\n')

    # Initialize a flag to start capturing data
    languages = []
    start_parsing = False

    for line in lines:
        if "Language coverage" in line:
            start_parsing = True
            continue

        if start_parsing:
            if line.strip() == "":
                continue
            if '|' not in line:
                continue
            parts = line.split('|')
            if len(parts) >= 2:
                code = parts[1].strip()[1:-1]
                identifier = parts[2].strip()[1:-1]
                name = parts[3].strip()
                languages.append({"code": code, "identifier": identifier, "name": name})

    # Omit the labels and divider
    languages = languages[2:] 

    # Convert to JSON
    json_data = json.dumps(languages, indent=4)

    # Save the JSON data to a file
    file_path = '/teamspace/studios/this_studio/multi-lang-translator/flores_language_codes.json'
    with open(file_path, 'w') as file:
        file.write(json_data)

    print(f"JSON data saved to {file_path}")

# generate_lang_code_file()

def get_language_code(language_name, 
                      json_file_path='/teamspace/studios/this_studio/multi-lang-translator/flores_language_codes.json'):
    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        languages = json.load(file)
    
    # Search for the language code by language name
    for language in languages:
        if language['name'].lower() == language_name.lower():
            return language['code']
    
    return None  # Return None if the language name is not found

def get_language_list(
                json_file_path='/teamspace/studios/this_studio/multi-lang-translator/flores_language_codes.json'):
    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        languages = json.load(file)
    
    # extract language name
    language_names = [language['name'] for language in languages]
    return language_names