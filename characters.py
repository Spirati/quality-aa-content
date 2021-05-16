import re
import requests
from bs4 import BeautifulSoup
import json

AA_WIKI_URL = "https://aceattorney.fandom.com"

CHARACTERS = []

def initial_character_list() -> None:
    birth_years_page = requests.get(f"{AA_WIKI_URL}/wiki/Category:Birth_years")
    if not birth_years_page.text:
        raise RuntimeError("fucking god damn it all to hell (initial category)")
    birth_years = BeautifulSoup(birth_years_page.text, features="html5lib")
    links = [tag["href"] for tag in filter(lambda a: "18" not in a["title"] and re.search(R"\d", a["title"]), birth_years.find_all("a", class_="category-page__member-link"))]

    for i,link in enumerate(links):
        print(f"Getting initial character list ({i+1}/{len(links)})", end="\r")
        characters_request = requests.get(f"{AA_WIKI_URL}{link}")
        if not characters_request.text:
            raise RuntimeError(f"fucking god damn it all to hell ({link})")
        characters = BeautifulSoup(characters_request.text, features="html5lib")
        character_list = characters.find_all("a",class_="category-page__member-link")
        CHARACTERS.extend([tag["title"].replace(" ","_") for tag in character_list])

def generate_character_list(use_stored: bool) -> dict: # string key for character name, list of mugshot images

    final_character_list = dict()

    if use_stored:
        try:
            with open("conf/character_info.json") as info:
                final_character_list = json.load(info)
        except:
            generate_character_list(False)
    
    else:
        initial_character_list()
        print()
        for i,character in enumerate(CHARACTERS):
            print("Filtering character list (%2.2f%%)" % (100*((i+1)/len(CHARACTERS))), end="\r")
            character_image_gallery_request = requests.get(f"{AA_WIKI_URL}/wiki/{character}_-_Image_Gallery")
            if not character_image_gallery_request.text:
                raise RuntimeError(f"fucking god damn it all to hell ({character})")
            if character_image_gallery_request.status_code == 404: continue

            character_image_gallery = BeautifulSoup(character_image_gallery_request.text, features="html5lib")
            mugshot_tab = character_image_gallery.find("div",class_="tabbertab",title="Mugshots")
            
            if mugshot_tab is None: continue

            final_character_list[character.replace("_"," ")] = list(map(lambda tag: AA_WIKI_URL + tag["href"], mugshot_tab.find_all("a", class_="image")))

        with open("conf/character_info.json", "w") as info:
            json.dump(final_character_list, info)
    
    return final_character_list
